from langchain.callbacks.base import BaseCallbackHandler

class StreamingCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str) -> None:
        print(f"My custom handler, token: {token}")
        