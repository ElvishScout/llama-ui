import os
import sys
import argparse
import json
from pathlib import Path

from env import *
from session import *
from chat import Chat


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


def ask(message: str, default: bool) -> bool:
    while True:
        reply = input(f"{message} ({'Y/n' if default else 'y/N'}) ").strip().lower()
        reply = reply or ("y" if default else "n")
        if reply == "y":
            return True
        elif reply == "n":
            return False


def start_chat(session: Session):
    user_name = session.user
    ai_name = session.character.name
    chat = Chat(session)

    greeting = chat.greet()
    if greeting is not None:
        print(f"=== {ai_name} ===")
        print(greeting)

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


def cli(args):
    session_path: str | Path
    is_new = True
    if args.session:
        session_path = args.session
        is_new = False
    else:
        session_path = ASSET_DIR / "template.json"

    with open(session_path, "r", encoding="utf-8") as f:
        session = Session.model_validate_json(f.read(), strict=False)

    if args.model:
        session.model = args.model
    if args.character:
        character: Character
        with open(args.character, "r", encoding="utf-8") as f:
            character = Character.model_validate_json(f.read(), strict=False)
        session.character = character
    if args.names:
        session.user = args.names[0]
        session.character.name = args.names[1]
    if args.prompt:
        for message in session.character.context:
            if message.role == "system":
                message.content = args.prompt
                break
        else:
            session.character.context.append(ChatMessage(role="system", content=args.prompt))

    if session.model == "":
        raise ValueError("no model specified")

    with supress_stderr():
        start_chat(session)

    save: bool
    try:
        save = ask("Save session?", True)
        if save:
            session_path = input(f"Enter session name: ").strip() or session_path
    except KeyboardInterrupt:
        save = False

    if save:
        with open(session_path, "w", encoding="utf-8") as f:
            f.write(session.model_dump_json(indent=2))


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

    session_path: Path
    is_new = True
    if args.session:
        session_path = Path(args.session)
        is_new = False
    else:
        session_path = ASSET_DIR / "template.json"

    session = Session.load_file(session_path)

    if args.model:
        session.model = args.model
    if args.names:
        session.user = args.names[0]
        session.character.name = args.names[1]
    if args.prompt:
        session.character.context.append(ChatMessage(role="system", content=args.prompt))

    if session.model == "":
        raise ValueError("no model specified")

    cli(session, is_new)
