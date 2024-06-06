import os
import sys
import argparse
import json
from pathlib import Path

from config import *
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


def ask(message: str, default: bool) -> bool | None:
    reply = input(message).strip().lower()
    reply = reply or ("y" if default else "n")
    if reply == "y":
        return True
    elif reply == "n":
        return False
    return None


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


def cli(session: Session, session_path: str):
    if session.model == "":
        raise ValueError("no model specified")

    with supress_stderr():
        start_chat(session)

    save: bool | None
    try:
        while True:
            save = ask("Save session? (Y/n)", True)
            if save is not None:
                break
        if save:
            while True:
                session_path = input(f"Enter session name: ").strip() or session_path
                if session_path != "":
                    break
    except KeyboardInterrupt:
        save = False

    if save:
        with open(session_path, "w", encoding="utf-8") as f:
            f.write(session.model_dump_json(indent=2))
