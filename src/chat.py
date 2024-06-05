from typing import *
import llama_cpp
from llama_cpp import Llama

from session import *


class Chat:
    def __init__(self, session: Session):
        self.session = session
        self.llm = Llama(session.model)
        self.context = self.session.character.context
        self.greeting = self.session.character.greeting
        self.history = self.session.history

    def greet(self) -> str | None:
        if len(self.history) == 0 and self.greeting is not None:
            self.history.append(ChatMessage(role="ai", content=self.greeting))
            return self.greeting
        return None

    def question(self, text: str) -> Generator[str, None, None]:
        self.history.append(ChatMessage(role="user", content=text))
        messages = [msg.model_dump() for msg in self.context + self.history]

        output = self.llm.create_chat_completion(messages, stream=True, **self.session.parameters.to_kwargs())
        answer = ""
        for chunk in output:
            delta = chunk["choices"][0]["delta"]
            if "role" in delta:
                pass
            elif "content" in delta:
                content = delta["content"] or ""
                answer += content
                yield content

        self.history.append(ChatMessage(role="ai", content=answer))
