import json
import shlex
from pathlib import Path
from typing import *
from pydantic import BaseModel
from llama_cpp import LlamaGrammar


builtin_stops = ["<|im_end|>"]


class ChatMessage(BaseModel):
    role: Literal["system", "user", "ai"]
    content: str


class Character(BaseModel):
    name: str
    context: list[ChatMessage]
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
                    kwargs[param] = builtin_stops + shlex.split(value)
                case "seed":
                    if value != -1:
                        kwargs[param] = value
                case "response_format":
                    if value != "":
                        kwargs[param] = json.loads(value)
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
    history: list[ChatMessage]
    parameters: Parameters

    @classmethod
    def load_file(cls, file: str | Path) -> Self:
        with open(file, "r", encoding="utf-8") as f:
            return cls(**json.load(f))
