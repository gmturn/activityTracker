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
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)

        # Adding Tab View
        self.mainTabView.add("Add Entry")
        self.mainTabView.add("Remove Entry")
        self.mainTabView.add("Tab 3")
        self.mainTabView.set("Add Entry")  # sets default to tab 1

        self.mainTabView.grid(row=0, column=0, padx=(
            20, 0), pady=(20, 0), sticky="NESW")  # sets location of the entire tab

        # Formatting Tab View
        self.mainTabView.grid_columnconfigure((0, 1, 2), weight=1)

        # Adding Add Entry Label
        addEntryLabel = ctk.CTkLabel(
            self.mainTabView.tab("Add Entry"), text="Add an Entry", font=ctk.CTkFont(size=20, weight="bold"))
        addEntryLabel.grid(row=0, column=1, padx=20, pady=20)

        # Adding Activity Section
        activtyLabel = ctk.CTkLabel(self.mainTabView.tab(  # creating the label for the activity drop down
            "Add Entry"), text="Activity Name:")
        activtyLabel.grid(row=1, column=0, padx=20)
        activities = self.entryManager.getActivityList()
        activities.sort()
        self.activityOptionMenu = ctk.CTkOptionMenu(self.mainTabView.tab("Add Entry"), dynamic_resizing=False,
                                                    values=activities)
        self.activityOptionMenu.grid(row=2, column=0, padx=50)

        # Adding Start Date and Time Section
        activtyLabel = ctk.CTkLabel(self.mainTabView.tab(  # creating the label for teh activity drop down
            "Add Entry"), text="Select Start Date:")
        activtyLabel.grid(row=1, column=1, padx=50)
        self.calendar = Calendar(self.mainTabView.tab(  # creating the label for teh activity drop down
            "Add Entry"), selectmode='day',
            year=2023, month=5,
            day=22)
        self.calendar.grid(row=2, column=1)

        # Adding End Date and Time Section
        activtyLabel = ctk.CTkLabel(self.mainTabView.tab(  # creating the label for the activity drop down
            "Add Entry"), text="Select End Date:")
        activtyLabel.grid(row=1, column=2, padx=50)
        self.calendar = Calendar(self.mainTabView.tab(  # creating the label for the activity drop down
            "Add Entry"), selectmode='day',
            year=2023, month=5,
            day=22)
        self.calendar.grid(row=2, column=2)

        # Adding Add Entry Button
        button = ctk.CTkButton(self.mainTabView.tab(
            "Add Entry"), text="Add Entry", font=ctk.CTkFont(size=18, weight="bold"))
        button.grid(row=5, column=1, padx=20, pady=20)
