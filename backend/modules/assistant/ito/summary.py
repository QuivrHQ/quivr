import tempfile

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
from modules.assistant.dto.outputs import (
    AssistantOutput,
    InputFile,
    Inputs,
    OutputBrain,
    OutputEmail,
    Outputs,
)
from modules.assistant.ito.ito import ITO

logger = get_logger(__name__)


class SummaryAssistant(ITO):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    async def process_assistant(self):

        # Create a temporary file with the uploaded file as a temporary file and then pass it to the loader
        tmp_file = tempfile.NamedTemporaryFile(delete=False)

        # Write the file to the temporary file
        tmp_file.write(self.uploadFile.file.read())

        # Now pass the path of the temporary file to the loader

        loader = UnstructuredPDFLoader(tmp_file.name)

        tmp_file.close()

        data = loader.load()

        llm = ChatLiteLLM(model="gpt-3.5-turbo")

        map_template = """The following is a set of documents
        {docs}
        Based on this list of docs, please identify the main themes 
        Helpful Answer:"""
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        # Reduce
        reduce_template = """The following is set of summaries:
        {docs}
        Take these and distill it into a final, consolidated summary of the main themes. 
        Helpful Answer:"""
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
            content, self.uploadFile.filename, "Summary"
        )


def summary_inputs():
    output = AssistantOutput(
        name="Summary",
        description="Summarize a set of documents",
        input_description="One document to summarize",
        output_description="A summary of the document",
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
