import ctypes
from typing import *
from tkinter import *
from tkinter import font
from tkinter.ttk import *
from tkinter.filedialog import *

from chat import Chat
from parameters import parameters

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class InputBox(Toplevel):
    def __init__(self, root: Tk):
        self.root = root
        root.wm_attributes("-toolwindow", True)
        root.columnconfigure(index=0, weight=1)

        self.create_widget(root)

        self.entry.focus()

    def create_widget(self, root):
        entry = self.entry = Entry(root)
        entry.grid(row=0, column=0, padx=5, pady=3, sticky="ew")

        frame_buttons = Frame(root)
        frame_buttons.grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        frame_buttons.columnconfigure(index=0, weight=1)

        button_save = Button(frame_buttons, text="Save")
        button_save.grid(row=0, column=1, padx=2, pady=2)

        button_cancel = Button(frame_buttons, text="Cancel")
        button_cancel.grid(row=0, column=2, padx=2, pady=2)


class TextEditor:
    def __init__(self, root: Tk):
        self.root = root
        root.geometry("800x600")
        root.wm_attributes("-toolwindow", True)
        root.rowconfigure(index=0, weight=1)
        root.columnconfigure(index=0, weight=1)

        self.create_widget(root)

        self.text.focus()

    def create_widget(self, root):
        text = self.text = Text(root)
        text.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")

        frame_buttons = Frame(root)
        frame_buttons.grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        frame_buttons.columnconfigure(index=0, weight=1)

        button_save = Button(frame_buttons, text="Save")
        button_save.grid(row=0, column=1, padx=2, pady=2)

        button_cancel = Button(frame_buttons, text="Cancel")
        button_cancel.grid(row=0, column=2, padx=2, pady=2)


class SessionSettings:
    def __init__(self, root: Tk):
        self.root = root
        root.geometry("400x600")
        root.wm_attributes("-toolwindow", True)
        root.title("Session Settings")

        self.create_widget(root)

        root.focus()

    def create_widget(self, root: Tk):
        root.rowconfigure(index=1, weight=1)
        root.columnconfigure(index=0, weight=1)

        lframe_basic = LabelFrame(root, text="Basic")
        lframe_basic.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        lframe_basic.columnconfigure(index=1, weight=1)

        label_model_path = Label(lframe_basic, text="Model Path")
        label_model_path.grid(row=0, column=0, padx=2, pady=2, sticky="w")

        frame_model_path = Frame(lframe_basic)
        frame_model_path.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        frame_model_path.columnconfigure(index=0, weight=1)

        entry_model_path = Entry(frame_model_path)
        entry_model_path.grid(row=0, column=0, sticky="ew")

        button_model_path = Button(
            frame_model_path, text="...", width=2, command=lambda *_: self.on_select_model_click()
        )
        button_model_path.grid(row=0, column=1)

        label_user_name = Label(lframe_basic, text="User Name")
        label_user_name.grid(row=1, column=0, padx=2, pady=2, sticky="w")

        entry_user_name = Entry(lframe_basic)
        entry_user_name.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        label_ai_name = Label(lframe_basic, text="AI Name")
        label_ai_name.grid(row=2, column=0, padx=2, pady=2, sticky="w")

        entry_ai_name = Entry(lframe_basic)
        entry_ai_name.grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        label_messages = Label(lframe_basic, text="Chat Messages")
        label_messages.grid(row=3, column=0, padx=2, pady=2, sticky="w")

        button_messages = Button(lframe_basic, text="Edit", command=lambda *_: self.on_edit_click())
        button_messages.grid(row=3, column=1, padx=2, pady=2, sticky="ew")

        lframe_adv = LabelFrame(root, text="Advanced")
        lframe_adv.grid(row=1, column=0, padx=5, pady=3, sticky="nsew")

        frame_adv = Frame(lframe_adv)
        frame_adv.pack(fill="both", expand=1, padx=2, pady=2)

        columns = ["Parameter", "Value"]
        tree_adv = self.tree_adv = Treeview(frame_adv, columns=columns, show="headings", selectmode="browse")
        tree_adv.pack(side="left", fill="both", expand=1)
        for i, column in enumerate(columns):
            tree_adv.column(i, minwidth=0, width=0, stretch=True)
            tree_adv.heading(i, text=column, anchor="w")

        scroll_adv = Scrollbar(frame_adv)
        scroll_adv.pack(side="right", fill="y")

        tree_adv.config(yscrollcommand=scroll_adv.set)
        scroll_adv.config(command=tree_adv.yview)

        for param, [decode, value, desc] in parameters.items():
            tree_adv.insert("", "end", values=[param, value])

        lframe_desc = LabelFrame(root, text="Description")
        lframe_desc.grid(row=2, column=0, padx=5, pady=3, sticky="nsew")

        text_desc = self.text_desc = Text(lframe_desc, height=4, state="disabled")
        text_desc.pack(fill="both", expand=1, padx=2, pady=2)

        frame_buttons = Frame(root)
        frame_buttons.grid(row=3, column=0, padx=5, pady=3, sticky="ew")
        frame_buttons.columnconfigure(index=0, weight=1)

        button_save = Button(frame_buttons, text="Save")
        button_save.grid(row=0, column=1, padx=2, pady=2)

        button_cancel = Button(frame_buttons, text="Cancel")
        button_cancel.grid(row=0, column=2, padx=2, pady=2)

        tree_adv.bind("<Double-1>", lambda ev: self.on_advanced_doubleclick(ev))
        tree_adv.bind("<ButtonRelease-1>", lambda *_: self.on_advanced_release())

    def on_select_model_click(self):
        model_path = askopenfilename(parent=self.root, title="Open Model", filetypes=[["GGUF File", ".gguf"]])

    def on_edit_click(self):
        editor = Toplevel(self.root)
        editor.title("Chat Messages")
        TextEditor(editor)
        editor.grab_set()
        editor.wait_window()
        self.root.grab_set()

    def on_advanced_doubleclick(self, ev):
        selections = self.tree_adv.selection()
        if not selections:
            return

        input_box = Toplevel(self.root)
        InputBox(input_box)
        input_box.title("New Value")
        input_box.geometry(f"+{ev.x_root - 20}+{ev.y_root - 20}")
        input_box.grab_set()
        input_box.wait_window()
        self.root.grab_set()

    def on_advanced_release(self):
        selections = self.tree_adv.selection()
        if not selections:
            return

        param_name = self.tree_adv.item(selections[0])["values"][0]
        desc = parameters[param_name][2]
        self.text_desc.config(state="normal")
        self.text_desc.delete("0.0", "end")
        self.text_desc.insert("end", desc)
        self.text_desc.config(state="disabled")


class ChatApp:
    def __init__(self, root: Tk):
        self.root = root
        root.geometry("1000x600")
        root.title("Llama")

        self.create_menu(root)
        self.create_widget(root)

    def create_menu(self, root: Tk):
        menu = Menu(root)

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
            underline=0,
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
            underline=0,
            accelerator="Ctrl+Shift+S",
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Preferences",
            command=self.preferences,
            underline=0,
            accelerator="Ctrl+P",
        )
        menu.add_cascade(label="File", menu=menu_file, underline=0)

        menu_edit = Menu(menu, tearoff=False)
        menu_edit.add_command(
            label="Session Settings",
            command=self.session_settings,
            underline=0,
        )

        menu.add_cascade(label="Edit", menu=menu_edit, underline=0)

        root.bind_all("<Control-n>", lambda *_: self.new_session())
        root.bind_all("<Control-Shift-n>", lambda *_: self.new_window())
        root.bind_all("<Control-o>", lambda *_: self.open_session())
        root.bind_all("<Control-s>", lambda *_: self.save())
        root.bind_all("<Control-Shift-s>", lambda *_: self.save_as())
        root.bind_all("<Control-p>", lambda *_: self.preferences())

        root.config(menu=menu)

    def create_widget(self, root: Tk):
        pass

    def new_window(self):
        pass

    def new_session(self):
        pass

    def open_session(self):
        file = askopenfile(parent=self.root, title="Open Session", filetypes=[["JSON File", ".json"]])
        if file is None:
            return

    def save(self):
        pass

    def save_as(self):
        pass

    def preferences(self):
        pass

    def session_settings(self):
        settings = Toplevel(self.root)
        SessionSettings(settings)
        settings.grab_set()
        settings.wait_window()
        self.root.grab_set()


if __name__ == "__main__":
    root = Tk()
    ChatApp(root)

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

    keys = ["family", "size", "weight", "slant", "underline", "overstrike"]
    for kind, font_args in app_fonts.items():
        kwargs = {keys[i]: value for i, value in enumerate(font_args) if value is not None}
        font.nametofont(f"Tk{kind}Font", root).configure(**kwargs)

    root.mainloop()
