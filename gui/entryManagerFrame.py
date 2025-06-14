import customtkinter as ctk
from managers.EntryManager import EntryManager
from tkinter import *
import tkinter as tk
from tkcalendar import Calendar
from gui.Operations import getCurrentDay, getCurrentMonth, getCurrentYearYYYY, getCurrenYearYY, convert_date_format
import datetime
from Models import EntryModel


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

        #
        # ADD ENTRY TAB
        #
        #
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
        activityComboBox = ctk.CTkComboBox(self.mainTabView.tab("Add Entry"),
                                           values=activities, variable=self.activityVar, state="readonly")
        activityComboBox.grid(row=2, column=0, padx=50)

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
        addEntryButton = ctk.CTkButton(self.mainTabView.tab(
            "Add Entry"), text="Add Entry", font=ctk.CTkFont(size=18, weight="bold"), command=self.addEntry)
        addEntryButton.grid(row=5, column=1, padx=20, pady=20)

        resetAddEntry = ctk.CTkButton(self.mainTabView.tab("Add Entry"), text="Reset Values", font=ctk.CTkFont(
            size=18, weight="bold"), command=self.clearAddEntryValues, fg_color="#CB2400", hover_color="#7B230F")
        resetAddEntry.grid(row=5, column=2, padx=20, pady=20)

        #
        # REMOVE ENTRY TAB
        #
        #
        # adding Remove Entry Label
        removeEntryLabel = ctk.CTkLabel(self.mainTabView.tab(
            "Remove Entry"), text="Remove an Entry", font=ctk.CTkFont(size=20, weight="bold"))
        removeEntryLabel.grid(row=0, column=1, padx=20, pady=20)

        selectDayLabel = ctk.CTkLabel(self.mainTabView.tab(
            "Remove Entry"), text="Select Day of Entry:")
        selectDayLabel.grid(row=1, column=0)

        self.removeEntryDay = Calendar(
            self.mainTabView.tab("Remove Entry"), selectmode='day')
        self.removeEntryDay.bind(
            "<<CalendarSelected>>", self.updateRemoveEntryListbox)
        self.removeEntryDay.grid(row=2, column=0)

        existingEntriesLabel = ctk.CTkLabel(self.mainTabView.tab(
            "Remove Entry"), text="Entries for the Selected Day:")
        existingEntriesLabel.grid(row=1, column=1)

        # Create listbox frame
        removeEntryListboxFrame = ctk.CTkFrame(
            self.mainTabView.tab("Remove Entry"))
        removeEntryListboxFrame.grid(row=2, column=1, padx=20)

        # Create a Scrollbar
        self.removeEntryScrollbar = tk.Scrollbar(
            removeEntryListboxFrame)
        self.removeEntryScrollbar.grid(
            row=0, column=1, sticky='ns')

        # Create a Listbox and associate it with the Scrollbar
        self.removeEntryListbox = tk.Listbox(
            removeEntryListboxFrame, state="normal",
            yscrollcommand=self.removeEntryScrollbar.set)
        self.removeEntryListbox.grid(row=0, column=0, sticky='ns')
        self.removeEntryListbox.bind(
            "<<ListboxSelect>>", self.showSelectedEntry)

        # Configure the Scrollbar to scroll the Listbox
        self.removeEntryScrollbar.config(command=self.removeEntryListbox.yview)
        self.updateRemoveEntryListbox()

        # Creating the Expanded Details section
        fullActivityLabel = ctk.CTkLabel(
            self.mainTabView.tab("Remove Entry"), text="Selected Entry Details:")
        fullActivityLabel.grid(row=1, column=2)

        self.removeEntryTextBox = ctk.CTkTextbox(
            self.mainTabView.tab("Remove Entry"))
        # self.removeEntryTextBox.configure(state="disabled")
        self.removeEntryTextBox.insert(
            "0.0", "Expanded details of the selected entry will be shown here.")
        self.removeEntryTextBox.grid(row=2, column=2)

        removeEntryButton = ctk.CTkButton(self.mainTabView.tab("Remove Entry"), text="Remove Entry", font=ctk.CTkFont(
            size=18, weight="bold"), command=self.removeEntry, fg_color="#CB2400", hover_color="#7B230F")
        removeEntryButton.grid(row=3, column=1)

    def getEntryDetails(self):
        # Verify input values
        error_messages = self.verifyAddEntryValues()
        if error_messages:
            # Show error messages to the user (you might want to replace this with a more user-friendly method)
            print(error_messages)
            return

        # Convert dates to "mm/dd/yyyy" format
        start_date = convert_date_format(self.startCalendar.get_date())
        end_date = convert_date_format(self.endCalendar.get_date())

        print(f"Activity: {self.activityVar.get()}")
        print(
            f"Start Time: {self.startHourVar.get()}:{self.startMinuteVar.get()}{self.start_am_pm.get()} {start_date}")
        print(
            f"End Time: {self.endHourVar.get()}:{self.endMinuteVar.get()}{self.end_am_pm.get()} {end_date}")

        self.clearAddEntryValues()

    def verifyAddEntryValues(self):
        error_messages = []

        # Verify activity selection
        if self.activityVar.get() == "Choose Activity":
            error_messages.append("Please select an activity.")

        # Verify start time selection
        if self.startHourMenu.get() == "Hour" or self.startMinuteMenu.get() == "Minutes":
            error_messages.append("Please select a start time.")

        # Verify end time selection
        if self.endHourMenu.get() == "Hour" or self.endMinuteMenu.get() == "Minutes":
            error_messages.append("Please select an end time.")

        # Handle case where date and/or time selections are out of range or incorrect format
        try:
            formatted_start_date = convert_date_format(
                self.startCalendar.get_date())
            formatted_end_date = convert_date_format(
                self.endCalendar.get_date())
            start_date = datetime.datetime.strptime(
                formatted_start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(
                formatted_end_date, "%Y-%m-%d")
            if start_date > end_date:
                error_messages.append(
                    "Start date can't be later than end date.")
        except ValueError:
            error_messages.append(
                "Invalid date format. Please correct your date selections.")

        try:
            start_hour = int(self.startHourMenu.get())
            end_hour = int(self.endHourMenu.get())
            start_minute = int(self.startMinuteMenu.get())
            end_minute = int(self.endMinuteMenu.get())
            if not (0 <= start_hour <= 12) or not (0 <= end_hour <= 12) or not (0 <= start_minute <= 59) or not (0 <= end_minute <= 59):
                error_messages.append(
                    "Invalid time format. Please correct your time selections.")
        except ValueError:
            error_messages.append(
                "Invalid time format. Please correct your time selections.")

        # Return any error messages
        if error_messages:
            return "\n".join(error_messages)
        else:
            return None

    def clearAddEntryValues(self):
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

    def getStartDateTime(self):
        startDay = self.startCalendar.get_date()
        startDateTime = datetime.datetime.strptime(
            convert_date_format(startDay), '%Y-%m-%d')

        # Change 12 am to 0
        startHour = self.startHourVar.get()
        startMinute = self.startMinuteVar.get()
        if startHour == 12 and self.start_am_pm.get() == "am":
            startHour = 0

        # Convert time to military time
        if self.start_am_pm.get() == "pm" and self.startHourVar.get() != 12:
            startHour += 12

        startDateTime = startDateTime.replace(
            hour=startHour, minute=startMinute)
        return startDateTime

    def getEndDateTime(self):
        endDay = self.endCalendar.get_date()
        endDateTime = datetime.datetime.strptime(
            convert_date_format(endDay), '%Y-%m-%d')

        # Change 12 am to 0
        endHour = self.endHourVar.get()
        endMinute = self.endMinuteVar.get()
        if endHour == 12 and self.end_am_pm.get() == "am":
            endHour = 0

        # Convert time to military time
        if self.end_am_pm.get() == "pm" and self.endHourVar.get() != 12:
            endHour += 12

        endDateTime = endDateTime.replace(
            hour=endHour, minute=endMinute)
        return endDateTime

    def addEntry(self):
        errorValues = self.verifyAddEntryValues()
        if errorValues:
            raise ValueError(
                "Error: Cannot add entry. Selected values are incorrect.")

        activity = self.activityVar.get()
        startDateTime = self.getStartDateTime()
        endDateTime = self.getEndDateTime()
        newEntry = EntryModel.Entry(activity, startDateTime, endDateTime)
        self.entryManager.addEntry(newEntry)
        self.clearAddEntryValues()

    def getEntriesOnSelectedDay(self):
        selectedDate = convert_date_format(self.removeEntryDay.get_date())
        entries = self.entryManager.getEntryList(
            datetime.datetime.strptime(selectedDate, '%Y-%m-%d'))
        values = []
        for entry in entries:
            values.append(entry)
        return values

    def updateRemoveEntryListbox(self, event=None):
        values = self.getEntriesOnSelectedDay()
        self.removeEntryListbox.delete(0, 'end')
        for i in range(0, len(values)):
            self.removeEntryListbox.insert(i + 1, values[i])

    def getListBoxIndex(self):
        index = self.removeEntryListbox.curselection()[0]
        return index

    def showSelectedEntry(self, event=None):
        # Get selected line index
        index = self.getListBoxIndex()
        entries = self.getEntriesOnSelectedDay()
        expandedDetails = entries[index].showExpandedDetails()

        self.removeEntryTextBox.configure(state="normal")
        self.removeEntryTextBox.delete("0.0", "end")
        self.removeEntryTextBox.insert(
            "0.0", expandedDetails)
        self.removeEntryTextBox.configure(state="disabled")

    def verifyRemoveEntry(self):
        index = self.removeEntryListbox.curselection()
        if index:
            return True

        else:
            return False

    def removeEntry(self):
        if not self.verifyRemoveEntry():
            print("Error: cannot remove a non-selected entry.")
            return

        index = self.getListBoxIndex()
        entries = self.getEntriesOnSelectedDay()
        self.entryManager.removeEntry(entries[index])
        self.updateRemoveEntryListbox()
        self.showSelectedEntry()
