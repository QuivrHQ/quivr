import tempfile
from typing import List

from fastapi import UploadFile
from langchain.chains import (
    MapReduceDocumentsChain,
    ReduceDocumentsChain,
    StuffDocumentsChain,
)
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatLiteLLM
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from logger import get_logger
from modules.assistant.dto.inputs import InputAssistant
from modules.assistant.dto.outputs import (
    AssistantOutput,
    InputFile,
    Inputs,
    OutputBrain,
    OutputEmail,
    Outputs,
)
from modules.assistant.ito.ito import ITO
from modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)


class SummaryAssistant(ITO):

    def __init__(
        self,
        input: InputAssistant,
        files: List[UploadFile] = None,
        current_user: UserIdentity = None,
        **kwargs,
    ):
        super().__init__(
            input=input,
            files=files,
            current_user=current_user,
            **kwargs,
        )

    def check_input(self):
        if not self.files:
            raise ValueError("No file was uploaded")
        if len(self.files) > 1:
            raise ValueError("Only one file can be uploaded")
        if not self.input.inputs.files:
            raise ValueError("No files key were given in the input")
        if len(self.input.inputs.files) > 1:
            raise ValueError("Only one file can be uploaded")
        if not self.input.inputs.files[0].key == "doc_to_summarize":
            raise ValueError("The key of the file should be doc_to_summarize")
        if not self.input.inputs.files[0].value:
            raise ValueError("No file was uploaded")
        # Check if name of file is same as the key
        if not self.input.inputs.files[0].value == self.files[0].filename:
            raise ValueError(
                "The key of the file should be the same as the name of the file"
            )
        if not (
            self.input.outputs.brain.activated or self.input.outputs.email.activated
        ):
            raise ValueError("No output was selected")
        return True

    async def process_assistant(self):

        try:
            self.increase_usage_user()
        except Exception as e:
            logger.error(f"Error increasing usage: {e}")
            return {"error": str(e)}

        # Create a temporary file with the uploaded file as a temporary file and then pass it to the loader
        tmp_file = tempfile.NamedTemporaryFile(delete=False)

        # Write the file to the temporary file
        tmp_file.write(self.files[0].file.read())

        # Now pass the path of the temporary file to the loader

        loader = UnstructuredPDFLoader(tmp_file.name)

        tmp_file.close()

        data = loader.load()

        llm = ChatLiteLLM(model="gpt-3.5-turbo", max_tokens=2000)

        map_template = """The following is one document to summarize that has been split into multiple sections:
        {docs}
        Based on the section, please identify the main themes, key points, and important information in each section.
        Helpful Knowledge in language of the document:"""
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        # Reduce
        reduce_template = """The following is set of summaries for each section of the document:
        {docs}
        Take these and distill it into a final, consolidated summary of the document. Make sure to include the main themes, key points, and important information.
        Use markdown such as bold, italics, underlined. For example, **bold**, *italics*, and _underlined_ to highlight key points.
        Please provide the final summary with sections using bold headers. 
        Sections should be: a short summary of the document called summary, and a list of key points called key points.
        Keep the same language as the documents.
        Summary:"""
        reduce_prompt = PromptTemplate.from_template(reduce_template)

        # Run chain
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs"
        )

        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=4000,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents(data)

        content = map_reduce_chain.run(split_docs)

        return await self.create_and_upload_processed_file(
            content, self.files[0].filename, "Summary"
        )


def summary_inputs():
    output = AssistantOutput(
        name="Summary",
        description="Summarize a set of documents",
        tags=["new"],
        input_description="One document to summarize",
        output_description="A summary of the document",
        icon_url="https://quivr-cms.s3.eu-west-3.amazonaws.com/assistant_summary_434446a2aa.png",
        inputs=Inputs(
            files=[
                InputFile(
                    key="doc_to_summarize",
                    allowed_extensions=["pdf"],
                    required=True,
                    description="The document to summarize",
                )
            ]
        ),
        outputs=Outputs(
            brain=OutputBrain(
                required=True,
                description="The brain to which upload the document",
                type="uuid",
            ),
            email=OutputEmail(
                required=True,
                description="Send the document by email",
                type="str",
            ),
        ),
    )
    return output
