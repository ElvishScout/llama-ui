import os
import argparse

from config import *
from session import *
from cli import cli

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Python UI for Llama chatbots.",
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
        "--char",
        dest="character",
        help="character file path",
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

    session: Session | None = None
    session_path = ""
    if args.session:
        session_path = args.session
        try:
            with open(session_path, "r", encoding="utf-8") as f:
                session = Session.model_validate_json(f.read(), strict=False)
        except FileNotFoundError:
            pass
    if session is None:
        with open(ASSET_DIR / "template.json", "r", encoding="utf-8") as f:
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
            session.character.context.append(Message(role="system", content=args.prompt))

    cli(session, session_path)
