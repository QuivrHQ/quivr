from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from models.chats import ChatMessage
from models.settings import BrainSettings
from pydantic import BaseModel  # For data validation and settings management
from supabase import Client  # For interacting with Supabase database
from supabase import create_client
from vectorstore.supabase import (
    CustomSupabaseVectorStore,
)  # Custom class for handling vector storage with Supabase


def get_chat_history(inputs) -> str:
    """
    Function to concatenate chat history into a single string.
    :param inputs: List of tuples containing human and AI messages.
    :return: concatenated string of chat history
    """
    res = []
    for human, ai in inputs:
        res.append(f"{human}:{ai}\n")
    return "\n".join(res)


class BrainPicking(BaseModel):
    """
    Main class for the Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    """

    # Default class attributes
    llm_name: str = "gpt-3.5-turbo"
    settings = BrainSettings()
    embeddings: OpenAIEmbeddings = None
    supabase_client: Client = None
    vector_store: CustomSupabaseVectorStore = None  # type: ignore
    llm: ChatOpenAI = None
    question_generator: LLMChain = None
    doc_chain: ConversationalRetrievalChain = None

    class Config:
        # Allowing arbitrary types for class validation
        arbitrary_types_allowed = True

    def init(self, model: str, user_id: str) -> "BrainPicking":
        """
        Initialize the BrainPicking class by setting embeddings, supabase client, vector store, language model and chains.
        :param model: Language model name to be used.
        :param user_id: The user id to be used for CustomSupabaseVectorStore.
        :return: BrainPicking instance
        """
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.settings.openai_api_key)
        self.supabase_client = create_client(
            self.settings.supabase_url, self.settings.supabase_service_key
        )
        self.vector_store = CustomSupabaseVectorStore(
            self.supabase_client, self.embeddings, table_name="vectors", user_id=user_id
        )
        self.llm = ChatOpenAI(temperature=0, model_name=model)
        self.question_generator = LLMChain(
            llm=self.llm, prompt=CONDENSE_QUESTION_PROMPT
        )
        self.doc_chain = load_qa_chain(self.llm, chain_type="map_reduce")
        return self

    def _get_qa(
        self, chat_message: ChatMessage, user_openai_api_key
    ) -> ConversationalRetrievalChain:
        """
        Retrieves a QA chain for the given chat message and API key.
        :param chat_message: The chat message containing history.
        :param user_openai_api_key: The OpenAI API key to be used.
        :return: ConversationalRetrievalChain instance
        """
        # If user provided an API key, update the settings
        if user_openai_api_key is not None and user_openai_api_key != "":
            self.settings.openai_api_key = user_openai_api_key

        # Initialize and return a ConversationalRetrievalChain
        qa = ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),
            max_tokens_limit=chat_message.max_tokens,
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,
        )
        return qa

    def generate_answer(self, chat_message: ChatMessage, user_openai_api_key) -> str:
        """
        Generate an answer to a given chat message by interacting with the language model.
        :param chat_message: The chat message containing history.
        :param user_openai_api_key: The OpenAI API key to be used.
        :return: The generated answer.
        """
        transformed_history = []

        # Get the QA chain
        qa = self._get_qa(chat_message, user_openai_api_key)

        # Transform the chat history into a list of tuples
        for i in range(0, len(chat_message.history) - 1, 2):
            user_message = chat_message.history[i][1]
            assistant_message = chat_message.history[i + 1][1]
            transformed_history.append((user_message, assistant_message))

        # Generate the model response using the QA chain
        model_response = qa(
            {"question": chat_message.question, "chat_history": transformed_history}
        )
        answer = model_response["answer"]

        return answer
