import ctypes
from typing import *
from tkinter import *
from tkinter import font
from tkinter.ttk import *
from tkinter.filedialog import *

from chat import Chat
from parameters import parameters

from pathlib import Path

# import chat
# import cli
# import gui
# import parameters

BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"
LOG_DIR = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "models"
SESSION_DIR = BASE_DIR / "sessions"

app_fonts = {
    "Default": ("微软雅黑", 9),
    "Text": ("微软雅黑", 9),
    "Fixed": ("微软雅黑", 9),
    "Menu": ("微软雅黑", 9),
    "Heading": ("微软雅黑", 9, "bold"),
    "Caption": ("微软雅黑", 9),
    "SmallCaption": ("微软雅黑", 9),
    "Icon": ("微软雅黑", 9),
    "Tooltip": ("微软雅黑", 9),
}


class InputBox(Toplevel):
    def __init__(self, parent: Tk):
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)
        self.columnconfigure(index=0, weight=1)

        self.create_widget()

        self.entry.focus()

    def create_widget(self):
        entry = self.entry = Entry(self)
        entry.grid(row=0, column=0, padx=5, pady=3, sticky="ew")

        frame_buttons = Frame(self)
        frame_buttons.grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        frame_buttons.columnconfigure(index=0, weight=1)

        button_save = Button(frame_buttons, text="Save")
        button_save.grid(row=0, column=1, padx=2, pady=2)

        button_cancel = Button(frame_buttons, text="Cancel")
        button_cancel.grid(row=0, column=2, padx=2, pady=2)


class TextEditor(Toplevel):
    def __init__(self, parent: Tk):
        super().__init__(parent)
        self.parent = parent
        self.geometry("800x600")
        self.transient(parent)
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        self.create_widget()

        self.text.focus()

    def create_widget(self):
        text = self.text = Text(self)
        text.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")

        frame_buttons = Frame(self)
        frame_buttons.grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        frame_buttons.columnconfigure(index=0, weight=1)

        button_save = Button(frame_buttons, text="Save")
        button_save.grid(row=0, column=1, padx=2, pady=2)

        button_cancel = Button(frame_buttons, text="Cancel")
        button_cancel.grid(row=0, column=2, padx=2, pady=2)


class SessionSettings(Toplevel):
    def __init__(self, parent: Tk):
        super().__init__(parent)
        self.parent = parent
        self.geometry("400x400")
        self.transient(parent)
        self.title("Session Settings")

        self.params: dict[str, Variable] = {}
        for param, [decode, value, desc] in parameters.items():
            self.params[param] = Variable(value=value)

        self.variables = {
            "model_path": Variable(value=""),
            "user_name": Variable(value="User"),
            "ai_name": Variable(value="AI"),
            "context": Variable(value=""),
            "history": Variable(value=""),
            "grammar": Variable(value=""),
            "response_format": Variable(value=""),
        }

        self.create_widget()

        self.focus()

    def create_widget(self):
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        notebook_settings = Notebook(self)
        notebook_settings.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")

        frame_basic = Frame(notebook_settings)
        notebook_settings.add(frame_basic, text="Basic")
        frame_basic.columnconfigure(index=1, weight=1)

        label_model_path = Label(frame_basic, text="Model Path")
        label_model_path.grid(row=0, column=0, padx=2, pady=2, sticky="w")

        frame_model_path = Frame(frame_basic)
        frame_model_path.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        frame_model_path.columnconfigure(index=0, weight=1)

        entry_model_path = Entry(frame_model_path, textvariable=self.variables["model_path"])
        entry_model_path.grid(row=0, column=0, sticky="ew")

        button_model_path = Button(
            frame_model_path, text="...", width=2, command=lambda *_: self.on_select_model_click()
        )
        button_model_path.grid(row=0, column=1)

        label_user_name = Label(frame_basic, text="User Name")
        label_user_name.grid(row=1, column=0, padx=2, pady=2, sticky="w")

        entry_user_name = Entry(frame_basic, self.variables["user_name"])
        entry_user_name.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        label_ai_name = Label(frame_basic, text="AI Name")
        label_ai_name.grid(row=2, column=0, padx=2, pady=2, sticky="w")

        entry_ai_name = Entry(frame_basic, self.variables["ai_name"])
        entry_ai_name.grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        label_context = Label(frame_basic, text="Context")
        label_context.grid(row=3, column=0, padx=2, pady=2, sticky="w")

        button_context = Button(frame_basic, text="Edit", command=lambda *_: self.on_edit_click())
        button_context.grid(row=3, column=1, padx=2, pady=2, sticky="ew")

        label_history = Label(frame_basic, text="History")
        label_history.grid(row=4, column=0, padx=2, pady=2, sticky="w")

        button_history = Button(frame_basic, text="Edit", command=lambda *_: self.on_edit_click())
        button_history.grid(row=4, column=1, padx=2, pady=2, sticky="ew")

        label_grammar = Label(frame_basic, text="Grammar")
        label_grammar.grid(row=5, column=0, padx=2, pady=2, sticky="w")

        button_grammar = Button(frame_basic, text="Edit")
        button_grammar.grid(row=5, column=1, padx=2, pady=2, sticky="ew")

        label_format = Label(frame_basic, text="Response Format")
        label_format.grid(row=6, column=0, padx=2, pady=2, sticky="w")

        button_format = Button(frame_basic, text="Edit")
        button_format.grid(row=6, column=1, padx=2, pady=2, sticky="ew")

        frame_adv = Frame(notebook_settings)
        notebook_settings.add(frame_adv, text="Advanced")
        frame_adv.rowconfigure(index=0, weight=1)
        frame_adv.columnconfigure(index=0, weight=1)

        frame_params = Frame(frame_adv)
        frame_params.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        frame_params.rowconfigure(index=0, weight=1)
        frame_params.columnconfigure(index=0, weight=1)

        frame_tree_entry = Frame(frame_params)
        frame_tree_entry.grid(row=0, column=0, sticky="nsew")
        frame_tree_entry.rowconfigure(index=0, weight=1)
        frame_tree_entry.columnconfigure(index=0, weight=1)

        columns = ["Parameter", "Value"]
        tree_params = self.tree_adv = Treeview(frame_tree_entry, columns=columns, show="headings", selectmode="browse")
        tree_params.grid(row=0, column=0, pady=2, sticky="nsew")
        for i, column in enumerate(columns):
            tree_params.column(i, minwidth=0, width=0, stretch=True)
            tree_params.heading(i, text=column, anchor="w")

        for param_name, variable in self.params:
            tree_params.insert("", "end", values=[param_name, variable.get()])

        entry_value = self.entry_param = Entry(frame_tree_entry)
        entry_value.grid(row=1, column=0, pady=2, sticky="ew")

        scroll_params = Scrollbar(frame_params)
        scroll_params.grid(row=0, column=1, rowspan=2, pady=2, sticky="ns")

        tree_params.config(yscrollcommand=scroll_params.set)
        scroll_params.config(command=tree_params.yview)

        frame_buttons = Frame(self)
        frame_buttons.grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        frame_buttons.columnconfigure(index=0, weight=1)

        button_save = Button(frame_buttons, text="Save")
        button_save.grid(row=0, column=1, padx=2, pady=2)

        button_cancel = Button(frame_buttons, text="Cancel")
        button_cancel.grid(row=0, column=2, padx=2, pady=2)

        tree_params.bind("<Double-1>", lambda ev: self.on_advanced_doubleclick(ev))
        tree_params.bind("<ButtonRelease-1>", lambda *_: self.on_advanced_release())

    def on_select_model_click(self):
        model_path = askopenfilename(parent=self, title="Open Model", filetypes=[["GGUF File", ".gguf"]])

    def on_edit_click(self):
        editor = TextEditor(self)
        editor.title("Chat Messages")
        editor.grab_set()
        editor.wait_window()
        self.grab_set()

    def on_advanced_doubleclick(self, ev: Event):
        selections = self.tree_adv.selection()
        if not selections:
            return

        input_box = InputBox(self)
        input_box.title("New Value")
        input_box.geometry(f"+{ev.x_root - 20}+{ev.y_root - 20}")
        input_box.grab_set()
        input_box.wait_window()
        self.grab_set()

    def on_advanced_release(self):
        selections = self.tree_adv.selection()
        if not selections:
            return

        param_name = self.tree_adv.item(selections[0])["values"][0]
        self.entry_param.config(textvariable=self.params[param_name])


class FontSettings(Toplevel):
    pass


class ChatApp(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("Llama")

        self.create_menu()
        self.create_widget()

    def create_menu(self):
        menu = Menu(self)

        menu_file = Menu(menu, tearoff=False)
        menu_file.add_command(
            label="New Session",
            command=self.new_session,
            underline=0,
            accelerator="Ctrl+N",
        )
        menu_file.add_command(
            label="New Window",
            command=self.new_session,
            underline=4,
            accelerator="Ctrl+Shift+N",
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Open Session",
            command=self.open_session,
            underline=0,
            accelerator="Ctrl+O",
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Save",
            command=self.save,
            underline=0,
            accelerator="Ctrl+S",
        )
        menu_file.add_command(
            label="Save As...",
            command=self.save_as,
            underline=5,
            accelerator="Ctrl+Shift+S",
        )
        menu.add_cascade(
            label="File",
            menu=menu_file,
            underline=0,
        )

        menu_edit = Menu(menu, tearoff=False)
        menu_edit.add_command(
            label="Session Settings",
            command=self.session_settings,
            underline=0,
        )
        menu_edit.add_separator()
        menu_edit.add_checkbutton(
            label="Show Logs",
            underline=5,
        )
        menu.add_cascade(
            label="Edit",
            menu=menu_edit,
            underline=0,
        )

        menu_pref = Menu(menu, tearoff=False)
        menu_pref.add_command(
            label="Font",
            command=self.font_settings,
            underline=0,
        )
        menu.add_cascade(
            label="Preferences",
            menu=menu_pref,
            underline=0,
        )

        self.bind_all("<Control-n>", lambda *_: self.new_session())
        self.bind_all("<Control-Shift-n>", lambda *_: self.new_window())
        self.bind_all("<Control-o>", lambda *_: self.open_session())
        self.bind_all("<Control-s>", lambda *_: self.save())
        self.bind_all("<Control-Shift-s>", lambda *_: self.save_as())
        self.bind_all("<Control-p>", lambda *_: self.preferences())

        self.config(menu=menu)

    def create_widget(self):
        paned_chat = PanedWindow(self, orient="vertical")
        paned_chat.pack(fill="both", expand=1, padx=5, pady=3)

        frame_history = Frame(paned_chat)
        paned_chat.add(frame_history, weight=1)

        text_history = Text(frame_history, width=0)
        text_history.pack(side="left", fill="both", expand=1)

        scroll_history = Scrollbar(frame_history)
        scroll_history.pack(side="right", fill="y")

        text_history.config(yscrollcommand=scroll_history.set)
        scroll_history.config(command=text_history.yview)

        frame_input = Frame(paned_chat)
        paned_chat.add(frame_input, weight=0)

        text_input = Text(frame_input, height=6, autoseparators=True)
        text_input.pack(fill="both", expand=1)

        for i in range(50):
            entry = Label(text_history, text="hello")
            text_history.window_create("insert", window=entry)
            text_history.insert("end", "\n")

    def new_window(self):
        pass

    def new_session(self):
        pass

    def open_session(self):
        file = askopenfile(parent=self, title="Open Session", filetypes=[["JSON File", ".json"]])
        if file is None:
            return

    def save(self):
        pass

    def save_as(self):
        pass

    def preferences(self):
        pass

    def session_settings(self):
        settings = SessionSettings(self)
        settings.grab_set()
        settings.wait_window()
        self.grab_set()

    def font_settings(self):
        pass


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    app = ChatApp()

    keys = ["family", "size", "weight", "slant", "underline", "overstrike"]
    for kind, font_args in app_fonts.items():
        kwargs = {keys[i]: value for i, value in enumerate(font_args) if value is not None}
        font.nametofont(f"Tk{kind}Font", app).configure(**kwargs)

    app.mainloop()
