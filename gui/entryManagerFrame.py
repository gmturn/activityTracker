import customtkinter as ctk
from tkinter import StringVar, Label, Entry
from managers.EntryManager import EntryManager
from tkinter import *
from tkcalendar import Calendar
from gui.Operations import getCurrentDay, getCurrentMonth, getCurrentYearYYYY, getCurrenYearYY


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
        self.activityVar = ctk.StringVar()
        self.activityVar.set("Choose Activity")
        activityOptionMenu = ctk.CTkOptionMenu(self.mainTabView.tab("Add Entry"), dynamic_resizing=False,
                                               values=activities, variable=self.activityVar)
        activityOptionMenu.grid(row=2, column=0, padx=50)

        # Adding Start Date and Time Section
        startDateLabel = ctk.CTkLabel(self.mainTabView.tab(  # creating the label for the Start Date calendar
            "Add Entry"), text="Select Start Date:")
        startDateLabel.grid(row=1, column=1, padx=50)
        self.startCalendar = Calendar(self.mainTabView.tab(
            "Add Entry"), selectmode='day',
            year=getCurrentYearYYYY(), month=getCurrentMonth(),
            day=getCurrentDay())
        self.startCalendar.grid(row=2, column=1)

        startTimeLabel = ctk.CTkLabel(self.mainTabView.tab(
            "Add Entry"), text="Select Start Time:")
        startTimeLabel.grid(row=3, column=1, padx=50)

        # Setting up a smaller frame for the start time
        self.startHourVar = ctk.IntVar()
        startTimeFrame = ctk.CTkFrame(self.mainTabView.tab("Add Entry"))
        self.startHourMenu = ctk.CTkOptionMenu(
            startTimeFrame, values=[str(i) for i in range(1, 13)], variable=self.startHourVar)
        self.startHourMenu.grid(row=0, column=0)
        self.startHourMenu.set("Hour")

        self.startMinuteVar = ctk.IntVar()
        self.startMinuteMenu = ctk.CTkOptionMenu(
            startTimeFrame, values=[str(i) for i in range(0, 60, 5)], variable=self.startMinuteVar)
        self.startMinuteMenu.grid(row=0, column=1)
        self.startMinuteMenu.set("Minutes")

        self.start_am_pm = ctk.StringVar(value="am")
        start_am_pmSwitch = ctk.CTkSwitch(
            startTimeFrame, text="AM / PM", variable=self.start_am_pm, offvalue="am", onvalue="pm")
        start_am_pmSwitch.grid(row=1, column=0, columnspan=2)

        startTimeFrame.grid(row=4, column=1, padx=10)

        # Setting up a smaller frame for end time
        endTimeLabel = ctk.CTkLabel(self.mainTabView.tab(
            "Add Entry"), text="Select End Time:")
        endTimeLabel.grid(row=3, column=2, padx=10)

        endTimeFrame = ctk.CTkFrame(self.mainTabView.tab("Add Entry"))

        self.endHourVar = ctk.IntVar()
        self.endHourMenu = ctk.CTkOptionMenu(
            endTimeFrame, values=[str(i) for i in range(1, 13)], variable=self.endHourVar)
        self.endHourMenu.grid(row=0, column=0)
        self.endHourMenu.set("Hour")

        self.endMinuteVar = ctk.IntVar()
        self.endMinuteMenu = ctk.CTkOptionMenu(
            endTimeFrame, values=[str(i) for i in range(0, 60, 5)], variable=self.endMinuteVar)
        self.endMinuteMenu.grid(row=0, column=1)
        self.endMinuteMenu.set("Minutes")

        self.end_am_pm = ctk.StringVar(value="am")
        end_am_pmSwitch = ctk.CTkSwitch(
            endTimeFrame, text="AM / PM", variable=self.end_am_pm, offvalue="am", onvalue="pm")
        end_am_pmSwitch.grid(row=1, column=0, columnspan=2)
        endTimeFrame.grid(row=4, column=2, padx=10)

        # Adding End Date and Time Section
        endDateLabel = ctk.CTkLabel(self.mainTabView.tab(  # creating the label for the End Date calendar
            "Add Entry"), text="Select End Date:")
        endDateLabel.grid(row=1, column=2, padx=50)
        self.endCalendar = Calendar(self.mainTabView.tab(
            "Add Entry"), selectmode='day',
            year=getCurrentYearYYYY(), month=getCurrentMonth(),
            day=getCurrentDay())
        self.endCalendar.grid(row=2, column=2)

        # Adding Add Entry Button
        button = ctk.CTkButton(self.mainTabView.tab(
            "Add Entry"), text="Add Entry", font=ctk.CTkFont(size=18, weight="bold"), command=self.getEntryDetails)
        button.grid(row=5, column=1, padx=20, pady=20)

    def getEntryDetails(self):
        print(f"Activity: {self.activityVar.get()}")
        print(
            f"Start Time: {self.startHourVar.get()}:{self.startMinuteVar.get()}{self.start_am_pm.get()} {self.startCalendar.get_date()}")
        print(
            f"End Time: {self.endHourVar.get()}:{self.endMinuteVar.get()}{self.end_am_pm.get()} {self.endCalendar.get_date()}")
        self.activityVar.set("Choose Activity")
        self.startHourVar.set(0)
        self.startMinuteMenu.set(0)
        self.endHourVar.set(0)
        self.endMinuteVar.set(0)
        self.start_am_pm.set("am")
        self.end_am_pm.set("am")
        self.startHourMenu.set("Hour")
        self.startMinuteMenu.set("Minutes")
        self.endHourMenu.set("Hour")
        self.endMinuteMenu.set("Minutes")
