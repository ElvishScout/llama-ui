from typing import *
import llama_cpp
from llama_cpp import Llama

from session import *


class Chat:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.llm = Llama(session.model)

    def question(self, text: str) -> Generator[str, None, None]:
        context = self.session.character.context
        history = self.session.history

        history.append(ChatMessage(role="user", content=text))
        messages = [msg.model_dump() for msg in context + history]

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
        history.append(ChatMessage(role="ai", content=answer))
