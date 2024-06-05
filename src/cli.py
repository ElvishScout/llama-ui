import os
import sys
import argparse
import json

from env import *
from chat import Chat
from session import Session


def input_multiline():
    text = ""
    while True:
        line = input()
        if line[-1] == "\\":
            text += line[-1]
            text += "\n"
        else:
            text += line
            break
    return text


class supress_stderr:
    def __init__(self):
        pass

    def __enter__(self):
        self.devnull = open(os.devnull, "w", encoding="utf-8")
        self.stderr = sys.stderr
        sys.stderr = self.devnull

    def __exit__(self, *_):
        sys.stderr = self.stderr
        self.devnull.close()


def start_chat(session: Session):
    user_name = session.user
    ai_name = session.character.name
    chat = Chat(session)

    while True:
        print(f"=== {user_name} ===")
        try:
            text = input_multiline().strip()
        except KeyboardInterrupt:
            break
        print(f"=== {ai_name} ===")
        for content in chat.question(text):
            print(content, end="")
        print()

    save = False
    try:
        reply = input("Save session? (Y/n) ").strip().lower() or "y"
        if save := (reply == "y"):
            if not session:
                session = input("Enter session name: ")
    except KeyboardInterrupt:
        save = False
        print("Canceled.")

    if save:
        with open(session, "w", encoding="utf-8") as f:
            f.write(json.encoder.JSONEncoder(ensure_ascii=False, indent=2).encode(chat.messages))


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
        "-m",
        "--model",
        dest="model",
        help="gguf model path",
        required=True,
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

    session_name = args.session or None
    model_path = args.model
    names = args.names or default_names
    prompt = args.prompt or None

    if (n := len(names)) < 2:
        raise ValueError(f"2 names required, got {n}")

    with supress_stderr():
        start_chat(model_path, names, prompt, session_name)
