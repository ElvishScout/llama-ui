import os
import sys
import argparse
import json
from pathlib import Path

from env import *
from session import *
from chat import Chat
from cli import cli


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Python command line interface for Llama chatbots.",
    )
    parser.add_argument(
        dest="session",
        help="session path",
        nargs="?",
    )
    parser.add_argument(
        "-g",
        "--gui",
        dest="gui",
        help="launch graphic user interface",
    )
    parser.add_argument(
        "-m",
        "--model",
        dest="model",
        help="gguf model path",
        required=False,
    )
    parser.add_argument(
        "-c",
        "--character",
        dest="character",
        help="ai character file path",
        required=False,
    )
    parser.add_argument(
        "-n",
        "--names",
        dest="names",
        help="human and ai names, separated by comma",
        type=lambda s: s.split(","),
        required=False,
    )
    parser.add_argument(
        "-p",
        "--prompt",
        dest="prompt",
        help="prompt message",
        required=False,
    )
    args = parser.parse_args()

    cli(args)
