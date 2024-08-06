from quivr_core import ChatLLM
from quivr_core.config import LLMEndpointConfig
from quivr_core.llm import LLMEndpoint

if __name__ == "__main__":
    llm_endpoint = LLMEndpoint.from_config(LLMEndpointConfig(model="gpt-4o-mini"))
    chat_llm = ChatLLM(
        llm=llm_endpoint,
    )
    print(chat_llm.llm_endpoint.info())
    response = chat_llm.answer("Hello,what is your model?")
    print(response)
