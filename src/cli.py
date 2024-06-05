import os
import sys
import argparse
import json

from chat import Chat

# from app import BASE_PATH

is_pressed = None
try:
    from keyboard import is_pressed

    is_pressed("ctrl")
except:
    is_pressed = None

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")


def input_multiline():
    text = ""
    while True:
        if is_pressed and is_pressed("ctrl"):
            break
        try:
            line = input()
        except EOFError:
            break
        if text:
            text += "\n"
        text += line
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


default_prompt = """\
This is a conversation between User and Llama, a friendly chatbot. Llama is \
helpful, kind, honest, good at writing, and never fails to answer any requests \
immediately and with precision.\
"""

default_names = ["User", "Assistant"]


def start_chat(model_path: str, names: list[str], prompt: str | None, session: str | None):
    messages = None
    if session:
        try:
            with open(session, "r", encoding="utf-8") as f:
                messages = json.decoder.JSONDecoder(strict=False).decode(f.read())
        except FileNotFoundError:
            pass

    if prompt and messages:
        raise ValueError("cannot apply prompt to an existing session")

    chat = Chat(model_path)

    if prompt:
        chat.prompt(prompt)
    if messages:
        chat.load_messages(messages)

    while True:
        print(f"=== {names[0]} ===")
        try:
            text = input_multiline().strip()
        except KeyboardInterrupt:
            break
        print(f"=== {names[1]} ===")
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
