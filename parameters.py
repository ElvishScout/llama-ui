from typing import *
import shlex
import json

from llama_cpp import LlamaGrammar

decoder = json.decoder.JSONDecoder()

parameters: dict[str, tuple[Callable[[str], Any], str, str]] = {
    "temperature": (
        float,
        "0.2",
        "The temperature to use for sampling.",
    ),
    "top_p": (
        float,
        "0.95",
        'The top-p value to use for nucleus sampling. Nucleus sampling described in academic paper "The Curious Case of Neural Text Degeneration" https://arxiv.org/abs/1904.09751',
    ),
    "top_k": (
        int,
        "40",
        'The top-k value to use for sampling. Top-K sampling described in academic paper "The Curious Case of Neural Text Degeneration" https://arxiv.org/abs/1904.09751',
    ),
    "min_p": (
        float,
        "0.05",
        "The min-p value to use for minimum p sampling. Minimum P sampling as described in https://github.com/ggerganov/llama.cpp/pull/3841",
    ),
    "typical_p": (
        float,
        "1.0",
        "The typical-p value to use for sampling. Locally Typical Sampling implementation described in the paper https://arxiv.org/abs/2202.00666.",
    ),
    "stop": (
        shlex.split,
        "",
        "A list of strings to stop generation when encountered.",
    ),
    "seed": (
        int,
        "",
        "The seed to use for sampling",
    ),
    "max_tokens": (
        int,
        "",
        "The maximum number of tokens to generate. If max_tokens <= 0 or None, the maximum number of tokens to generate is unlimited and depends on n_ctx.",
    ),
    "presence_penalty": (
        float,
        "0.0",
        "The penalty to apply to tokens based on their presence in the prompt.",
    ),
    "frequency_penalty": (
        float,
        "0.0",
        "The penalty to apply to tokens based on their frequency in the prompt.",
    ),
    "repeat_penalty": (
        float,
        "1.1",
        "The penalty to apply to repeated tokens.",
    ),
    "tfs_z": (
        float,
        "1.0",
        "The tail-free sampling parameter.",
    ),
    "mirostat_mode": (
        int,
        "0",
        "The mirostat sampling mode.",
    ),
    "mirostat_tau": (
        float,
        "5.0",
        "The mirostat sampling tau parameter.",
    ),
    "mirostat_eta": (
        float,
        "0.1",
        "The mirostat sampling eta parameter.",
    ),
    "logit_bias": (
        decoder.decode,
        "",
        "A logit bias to use.",
    ),
    "logprobs": (
        bool,
        "",
        "",
    ),
    "top_logprobs": (
        int,
        "",
        "",
    ),
}
