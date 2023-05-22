import customtkinter as ctk
from tkinter import StringVar, Label, Entry
from managers.EntryManager import EntryManager
from tkinter import *
from tkcalendar import Calendar


class EntryManagerFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)

        self.entryManager = EntryManager()
        self.mainTabView = ctk.CTkTabview(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 1), weight=1)

        self.mainTabView.add("Tab 1")
        self.mainTabView.add("Tab 2")
        self.mainTabView.add("Tab 3")
        self.mainTabView.set("Tab 1")  # sets default to tab 1

        self.mainTabView.grid(row=0, column=0, padx=20, pady=10, sticky="NESW")

        button = ctk.CTkButton(self.mainTabView.tab(
            "Tab 1"), text="Tab 1 Button")
        button.pack(padx=20, pady=20)

        # Set up your frame layout and widgets here

        # Set up buttons and bind them to functions to add or remove entries
