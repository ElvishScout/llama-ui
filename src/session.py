import json
import shlex
from pathlib import Path
from typing import *
from pydantic import BaseModel
from llama_cpp import (
    LlamaGrammar,
    ChatCompletionRequestResponseFormat as ResponseFormat,
)


builtin_stops = ["<|im_end|>"]


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class Character(BaseModel):
    name: str
    context: list[Message]
    greetings: Optional[Union[str, list[str]]]


class Parameters(BaseModel):
    max_tokens: Optional[int]
    temperature: float
    top_p: float
    top_k: int
    typical_p: float
    min_p: float
    repeat_penalty: float
    frequency_penalty: float
    presence_penalty: float
    stop: Optional[Union[str, list[str]]]
    seed: Optional[int]
    response_format: Optional[ResponseFormat]
    mirostat_mode: int
    mirostat_tau: float
    mirostat_eta: float
    tfs_z: float
    grammar: Optional[str]

    def to_kwargs(self) -> dict[str, Any]:
        kwargs = {}
        for param, value in self.model_dump().items():
            match (param):
                case "stop":
                    kwargs[param] = builtin_stops + ([value] if isinstance(value, str) else value)
                case "seed":
                    if value != -1:
                        kwargs[param] = value
                case "grammar":
                    if value != "":
                        kwargs[param] = LlamaGrammar.from_string(value)
                case _:
                    kwargs[param] = value
        return kwargs


class Session(BaseModel):
    model: str
    user: str
    character: Character
    history: list[Message]
    parameters: Parameters


if __name__ == "__main__":
    print(Session.model_json_schema())
