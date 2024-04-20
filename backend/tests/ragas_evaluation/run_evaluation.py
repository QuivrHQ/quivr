import argparse
import os
import sys

from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.append(os.getcwd())
# Load environment variables from .env file
load_dotenv(verbose=True, override=True)

import glob
import uuid

import pandas as pd
import ragas
from celery_worker import process_file_and_notify
from datasets import Dataset
from langchain_core.runnables.base import RunnableSerializable
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from modules.brain.rags.quivr_rag import QuivrRAG
from modules.brain.service.brain_service import BrainService
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.service.knowledge_service import KnowledgeService
from ragas import evaluate
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from modules.upload.service.upload_file import upload_file_storage


def main(
    testset_path, input_folder, output_folder, model, context_size, metrics, brain_id
):
    # Create a fake user and brain
    # Check if a brain ID was provided
    if args.brain_id:
        brain = brain_service.get_brain(args.brain_id)
        if not brain:
            print("Invalid brain ID provided.")
            sys.exit(1)
    else:
        # Create a new brain
        uuid_value = uuid.uuid4()
        brain_service = BrainService()
        knowledge_service = KnowledgeService()
        brain = brain_service.create_brain(user_id=uuid_value, brain=None)
    brain_id = brain.brain_id

    for document_path in glob.glob(input_folder + "/*"):
        # Process each document here
        process_document(knowledge_service, brain_id, document_path)

    # Load test data
    test_data = pd.read_json(testset_path)

    # Create a QuivrRAG chain
    knowledge_qa = QuivrRAG(
        model=model,
        brain_id=str(brain_id),
        chat_id=str(uuid.uuid4()),
        streaming=False,
        max_input=context_size,
        max_tokens=1000,
    )
    brain_chain = knowledge_qa.get_chain()

    # run langchain RAG
    response_dataset = generate_replies(test_data, brain_chain)

    ragas_metrics = [getattr(ragas.metrics, metric) for metric in metrics]
    score = evaluate(
        response_dataset,
        metrics=ragas_metrics,
        llm=ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1),
        embeddings=LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1536)
        ),
    ).to_pandas()

    score.to_json(output_folder + "/score.json", orient="records")
    for metric in metrics:
        print(f"{metric} mean score: {score[metric].mean()}")
        print(f"{metric} median score: {score[metric].median()}")
    # Cleanup if a new brain was created
    if not args.brain_id:
        brain_service.delete_brain(brain_id)


def process_document(
    knowledge_service: KnowledgeService, brain_id: uuid.UUID, document_path: str
) -> None:
    """
    Process a document by uploading it to the file storage, adding knowledge to the knowledge service,
    and then processing the file and sending a notification.

    Args:
        knowledge_service: The knowledge service object used to add knowledge.
        brain_id: The ID of the brain.
        document_path: The path of the document to be processed.

    Returns:
        None
    """
    filename = document_path.split("/")[-1]
    filename_with_brain_id = str(brain_id) + "/" + str(filename)
    file_in_storage = upload_file_storage(document_path, filename_with_brain_id)

    knowledge_to_add = CreateKnowledgeProperties(
        brain_id=brain_id,
        file_name=filename,
        extension=os.path.splitext(filename)[  # pyright: ignore reportPrivateUsage=none
            -1
        ].lower(),
    )

    added_knowledge = knowledge_service.add_knowledge(knowledge_to_add)
    print(f"Knowledge {added_knowledge} added successfully")

    process_file_and_notify(
        file_name=filename_with_brain_id,
        file_original_name=filename,
        brain_id=brain_id,
        notification_id=None,
    )


def generate_replies(
    test_data: pd.DataFrame, brain_chain: RunnableSerializable
) -> Dataset:
    """
    Generate replies for a given test data using a brain chain.

    Args:
        test_data (pandas.DataFrame): The test data containing questions and ground truths.
        brain_chain (RunnableSerializable): The brain chain to use for generating replies.

    Returns:
        Dataset: A dataset containing the generated replies, including questions, answers, contexts, and ground truths.
    """
    answers = []
    contexts = []
    test_questions = test_data.question.tolist()
    test_groundtruths = test_data.ground_truth.tolist()

    for question in test_questions:
        response = brain_chain.invoke({"question": question})
        answers.append(response["answer"].content)
        contexts.append([context.page_content for context in response["docs"]])

    return Dataset.from_dict(
        {
            "question": test_questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": test_groundtruths,
        }
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Ragas evaluation on a test dataset"
    )
    parser.add_argument(
        "--input_folder",
        type=str,
        required=True,
        help="Path to the testset documents folder",
    )
    parser.add_argument(
        "--output_folder", type=str, default="./", help="Path to the output folder"
    )
    parser.add_argument(
        "--testset_path", type=str, required=True, help="Path to the testset JSON file"
    )
    parser.add_argument(
        "--model", type=str, default="gpt-3.5-turbo-0125", help="Model to use"
    )
    parser.add_argument(
        "--context_size", type=int, default=4000, help="Context size for the model"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        nargs="+",
        choices=[
            "answer_correctness",
            "context_relevancy",
            "context_precision",
            "faithfulness",
            "answer_similarity",
        ],
        default=["answer_correctness"],
        help="Metrics to evaluate",
    )
    parser.add_argument(
        "--brain_id",
        type=str,
        default=None,
        help="ID of an existing brain to use for the evaluation",
    )
    args = parser.parse_args()

    main(
        args.testset_path,
        args.input_folder,
        args.output_folder,
        args.model,
        args.context_size,
        args.metrics,
        args.brain_id,
    )


# Run by doing from the backend folder:
# python3 tests/ragas_evaluation/run_evaluation.py --input_folder ./tests/input --testset_path ./tests/ragas_tests/experiment.json --context_size 1000
# Make sure to copy the .env file to the backend folder and modify http://host.docker.internal to http://localhost
# in the .env file
