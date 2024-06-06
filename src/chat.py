from typing import *
from llama_cpp import Llama
from random import choice

from session import *


class Chat:
    def __init__(self, session: Session):
        self.session = session
        self.llm = Llama(session.model)
        self.context = self.session.character.context
        self.greetings = self.session.character.greetings
        self.history = self.session.history

    def greet(self) -> str | None:
        if not self.history and self.greetings:
            content: str
            if isinstance(self.greetings, str):
                content = self.greetings
            else:
                content = choice(self.greetings)
            self.history.append(Message(role="assistant", content=content))
            return content
        return None

    def question(self, text: str) -> Generator[str, None, None]:
        self.history.append(Message(role="user", content=text))
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

        self.history.append(Message(role="assistant", content=answer))
