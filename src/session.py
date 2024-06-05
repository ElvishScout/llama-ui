import json
import shlex
from typing import *
from pydantic import *
from llama_cpp import *


class ChatMessage(BaseModel):
    role: Literal["system", "user", "ai"]
    content: str


class Character(BaseModel):
    char_name: str
    context: Optional[list[ChatMessage]]
    history: Optional[list[ChatMessage]]
    greeting: Optional[str]


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
    stop: Optional[str]
    seed: Optional[int]
    response_format: Optional[str]
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
                    kwargs[param] = shlex.split(value)
                case "seed":
                    if value != -1:
                        kwargs[param] = value
                case "response_format":
                    if value:
                        kwargs[param] = json.loads(value)
                case "grammar":
                    if value:
                        kwargs[param] = LlamaGrammar.from_string(value)
                case _:
                    kwargs[param] = value
        return kwargs


class Session(BaseModel):
    model: str
    user_name: str
    character: Character
    parameters: Parameters

    def load_file(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return Session(**json.load(f))


print(Session.load_file("./default.json").parameters.to_kwargs())
