import customtkinter as ctk
from tkinter import StringVar, Label, Entry
from managers.EntryManager import EntryManager


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)

        # Set up your frame layout and widgets here

        self.activity_label = ctk.CTkLabel(self, text="Home")
        self.activity_label.pack()  # adjust as needed

        # Set up buttons and bind them to functions to add or remove entries
        # ...
