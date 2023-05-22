import customtkinter as ctk
from tkinter import StringVar, Label, Entry
from managers.EntryManager import EntryManager


class EntryManagerFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)

        self.entryManager = EntryManager()

        # Set up your frame layout and widgets here

        self.activity_label = Label(self, text="Activity")
        self.activity_label.pack()  # adjust as needed

        self.activity_var = StringVar()
        self.activity_entry = Entry(self, textvariable=self.activity_var)
        self.activity_entry.pack()  # adjust as needed

        self.color_label = Label(self, text="Color")
        self.color_label.pack()  # adjust as needed

        self.color_var = StringVar()
        self.color_entry = Entry(self, textvariable=self.color_var)
        self.color_entry.pack()  # adjust as needed

        # Set up buttons and bind them to functions to add or remove entries
        # ...

    def add_entry(self):
        activity = self.activity_var.get()
        color = self.color_var.get()
        self.entryManager.addActivity(activity, color)
        # add additional processing and error handling as needed

    def remove_entry(self):
        activity = self.activity_var.get()
        self.entryManager.removeActivity(activity)
        # add additional processing and error handling as needed
