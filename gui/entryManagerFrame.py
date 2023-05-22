import customtkinter as ctk
from tkinter import StringVar, Label, Entry
from managers.EntryManager import EntryManager
from tkinter import *
from tkcalendar import Calendar


class EntryManagerFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)

        self.entryManager = EntryManager()
        self.mainTabView = ctk.CTkTabview(self, width=500)

        # Setting frame grid size, not too sure how it works
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 1), weight=1)

        self.mainTabView.add("Add Entry")
        self.mainTabView.add("Tab 2")
        self.mainTabView.add("Tab 3")
        self.mainTabView.set("Add Entry")  # sets default to tab 1

        self.mainTabView.grid(row=0, column=0, padx=(
            20, 0), pady=(20, 0), sticky="NESW")  # sets location of the entire tab

        button = ctk.CTkButton(self.mainTabView.tab(
            "Add Entry"), text="Add Entry Button")
        button.pack(padx=20, pady=20)

        # Set up your frame layout and widgets here

        # Set up buttons and bind them to functions to add or remove entries
