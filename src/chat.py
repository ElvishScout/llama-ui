from typing import *
import llama_cpp
from llama_cpp import Llama


class Chat:
    def __init__(self, model_path: str, metadata: dict[str, Any] = {}) -> None:
        self.metadata = metadata
        self.messages = []
        self.llm = Llama(model_path)

    def prompt(self, prompt: str) -> None:
        self.messages.append({"role": "system", "content": prompt})

    def load_messages(self, messages: list[dict[str, str]] = []):
        self.messages += messages

    def question(self, text: str) -> Generator[str, None, None]:
        self.messages.append({"role": "user", "content": text})
        output = self.llm.create_chat_completion(self.messages, stream=True, **self.metadata)
        answer = ""
        for chunk in output:
            delta = chunk["choices"][0]["delta"]
            if "role" in delta:
                pass
            elif "content" in delta:
                content = delta["content"] or ""
                answer += content
                yield content
        self.messages.append({"role": "assistant", "content": answer})
