import logging
from operator import itemgetter
from typing import AsyncGenerator

from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI
from quivr_api.modules.knowledge.entity.knowledge import Knowledge
from quivr_api.packages.quivr_core.config import RAGConfig
from quivr_api.packages.quivr_core.models import (
    ParsedRAGChunkResponse,
    ParsedRAGResponse,
    cited_answer,
)
from quivr_api.packages.quivr_core.prompts import (
    ANSWER_PROMPT,
    CONDENSE_QUESTION_PROMPT,
)
from quivr_api.packages.quivr_core.utils import (
    combine_documents,
    format_file_list,
    get_chunk_metadata,
    model_supports_function_calling,
    parse_chunk_response,
    parse_response,
)

logger = logging.getLogger(__name__)


class QuivrQARAG:
    def __init__(
        self,
        *,
        rag_config: RAGConfig,
        llm: ChatLiteLLM,
        vector_store: VectorStore,
    ):
        self.rag_config = rag_config
        self.vector_store = vector_store
        self.llm = llm
        self.reranker = self._create_reranker()
        self.supports_func_calling = model_supports_function_calling(
            self.rag_config.model
        )

    @property
    def retriever(self):
        return self.vector_store.as_retriever()

    def _create_reranker(self):
        # TODO: reranker config
        compressor = CohereRerank(top_n=20)
        # else:
        #     ranker_model_name = "ms-marco-TinyBERT-L-2-v2"
        #     flashrank_client = Ranker(model_name=ranker_model_name)
        #     compressor = FlashrankRerank(
        #         client=flashrank_client, model=ranker_model_name, top_n=20
        #     ) # TODO @stangirard fix
        return compressor

    # TODO : refactor and simplify
    def filter_history(
        self, chat_history, max_history: int = 10, max_tokens: int = 2000
    ):
        """
        Filter out the chat history to only include the messages that are relevant to the current question

        Takes in a chat_history= [HumanMessage(content='Qui est Chloé ? '), AIMessage(content="Chloé est une salariée travaillant pour l'entreprise Quivr en tant qu'AI Engineer, sous la direction de son supérieur hiérarchique, Stanislas Girard."), HumanMessage(content='Dis moi en plus sur elle'), AIMessage(content=''), HumanMessage(content='Dis moi en plus sur elle'), AIMessage(content="Désolé, je n'ai pas d'autres informations sur Chloé à partir des fichiers fournis.")]
        Returns a filtered chat_history with in priority: first max_tokens, then max_history where a Human message and an AI message count as one pair
        a token is 4 characters
        """
        chat_history = chat_history[::-1]
        total_tokens = 0
        total_pairs = 0
        filtered_chat_history = []
        for i in range(0, len(chat_history), 2):
            if i + 1 < len(chat_history):
                human_message = chat_history[i]
                ai_message = chat_history[i + 1]
                message_tokens = (
                    len(human_message.content) + len(ai_message.content)
                ) // 4
                if (
                    total_tokens + message_tokens > max_tokens
                    or total_pairs >= max_history
                ):
                    break
                filtered_chat_history.append(human_message)
                filtered_chat_history.append(ai_message)
                total_tokens += message_tokens
                total_pairs += 1
        chat_history = filtered_chat_history[::-1]

        return chat_history

    def build_chain(self, files: str):
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=self.reranker, base_retriever=self.retriever
        )

        loaded_memory = RunnablePassthrough.assign(
            chat_history=RunnableLambda(
                lambda x: self.filter_history(x["chat_history"]),
            ),
            question=lambda x: x["question"],
        )

        standalone_question = {
            "standalone_question": {
                "question": lambda x: x["question"],
                "chat_history": itemgetter("chat_history"),
            }
            | CONDENSE_QUESTION_PROMPT
            | self.llm
            | StrOutputParser(),
        }

        # Now we retrieve the documents
        retrieved_documents = {
            "docs": itemgetter("standalone_question") | compression_retriever,
            "question": lambda x: x["standalone_question"],
            "custom_instructions": lambda x: self.rag_config.prompt,
        }

        final_inputs = {
            "context": lambda x: combine_documents(x["docs"]),
            "question": itemgetter("question"),
            "custom_instructions": itemgetter("custom_instructions"),
            "files": lambda _: files,  # TODO: shouldn't be here
        }

        # Override llm if we have a OpenAI model
        llm = self.llm
        if self.supports_func_calling:
            if self.rag_config.temperature:
                llm_function = ChatOpenAI(
                    max_tokens=self.rag_config.max_tokens,
                    model=self.rag_config.model,
                    temperature=self.rag_config.temperature,
                )
            else:
                llm_function = ChatOpenAI(
                    max_tokens=self.rag_config.max_tokens,
                    model=self.rag_config.model,
                )

            llm = llm_function.bind_tools(
                [cited_answer],
                tool_choice="any",
            )

        answer = {
            "answer": final_inputs | ANSWER_PROMPT | llm,
            "docs": itemgetter("docs"),
        }

        return loaded_memory | standalone_question | retrieved_documents | answer

    def answer(
        self,
        question: str,
        history: list[dict[str, str]],
        list_files: list[Knowledge],
        metadata: dict[str, str] = {},
    ) -> ParsedRAGResponse:
        concat_list_files = format_file_list(list_files, self.rag_config.max_files)
        conversational_qa_chain = self.build_chain(concat_list_files)
        raw_llm_response = conversational_qa_chain.invoke(
            {
                "question": question,
                "chat_history": history,
                "custom_instructions": (self.rag_config.prompt),
            },
            config={"metadata": metadata},
        )
        response = parse_response(raw_llm_response, self.rag_config.model)
        return response

    async def answer_astream(
        self,
        question: str,
        history: list[dict[str, str]],
        list_files: list[Knowledge],
        metadata: dict[str, str] = {},
    ) -> AsyncGenerator[ParsedRAGChunkResponse, ParsedRAGChunkResponse]:
        concat_list_files = format_file_list(list_files, self.rag_config.max_files)
        conversational_qa_chain = self.build_chain(concat_list_files)

        rolling_message = AIMessageChunk(content="")
        sources = []

        async for chunk in conversational_qa_chain.astream(
            {
                "question": question,
                "chat_history": history,
                "custom_personality": (self.rag_config.prompt),
            },
            config={"metadata": metadata},
        ):
            # Could receive this anywhere so we need to save it for the last chunk
            if "docs" in chunk:
                sources = chunk["docs"] if "docs" in chunk else []

            if "answer" in chunk:
                rolling_message, parsed_chunk = parse_chunk_response(
                    rolling_message,
                    chunk,
                    self.supports_func_calling,
                )

                if self.supports_func_calling and len(parsed_chunk.answer) > 0:
                    yield parsed_chunk
                else:
                    yield parsed_chunk

        # Last chunk provies
        yield ParsedRAGChunkResponse(
            answer="",
            metadata=get_chunk_metadata(rolling_message, sources),
            last_chunk=True,
        )
