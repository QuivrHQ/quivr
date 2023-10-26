from llm.qa_headless import HeadlessQA
from routes.chat.interface import ChatInterface


class BrainlessChat(ChatInterface):
    def validate_authorization(self, user_id, brain_id):
        pass

    def get_answer_generator(
        self,
        brain_id,
        chat_id,
        model,
        max_tokens,
        temperature,
        user_openai_api_key,
        streaming,
        prompt_id,
    ):
        return HeadlessQA(
            chat_id=chat_id,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            user_openai_api_key=user_openai_api_key,
            streaming=streaming,
            prompt_id=prompt_id,
        )
