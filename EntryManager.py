import json
from colorama import init
from termcolor import colored
from Models.EntryModel import Entry
import os
import datetime


class EntryManager:
    def __init__(self):
        self.activities = {}
        self.activitiesJSON = "./data/activities.json"

        with open(self.activitiesJSON) as file:
            data = json.load(file)

        try:
            for item in data["activities"]:
                self.activities[item["activity"]] = item["color"]
        except:
            pass

    def addActivity(self, activity, color):
        with open(self.activitiesJSON, 'r') as file:
            data = json.load(file)

        # Check if an activity with the same name already exists
        for existing_activity in data['activities']:
            if existing_activity['activity'] == activity:
                print(
                    f"Error: An activity with the name '{activity}' already exists.")
                return

        # Append the new activity to the "activities" list
        activityDict = {
            "activity": activity,
            "color": color
        }

        data['activities'].append(activityDict)

        with open(self.activitiesJSON, 'w') as file:
            # indent parameter is used to make the output easy to read
            json.dump(data, file, indent=2)

    def removeActivity(self, activity):
        pass

    def addEntry(self, entry):
        if not isinstance(entry, Entry):
            raise ValueError(
                "Error: EntryManager.addEntry(entry) value is not type Entry.")

        startDateTime = entry.getStartTime()
        endDateTime = entry.getEndTime()
        currentDateTime = startDateTime

        while currentDateTime < endDateTime:
            nextDateTime = self.get_end_of_day_or_entry(
                currentDateTime, endDateTime)
            duration = nextDateTime - currentDateTime
            entryFile = self.get_entry_file_path(currentDateTime)
            entryData = self.create_entry_data(
                entry, currentDateTime, nextDateTime, duration)

            data = self.load_or_create_data(entryFile, entryData)

            if self.check_overlap(entryData, data["entries"]):
                raise ValueError("Error: Overlapping entry.")

            data = self.update_stats(data, entry, duration)
            self.save_to_file(entryFile, data)
            currentDateTime += datetime.timedelta(days=1)

    def removeEntry(self, entry):
        if not isinstance(entry, Entry):
            raise ValueError(
                "Error: EntryManager.removeEntry(entry) value is not type Entry.")

        startDateTime = entry.getStartTime()
        endDateTime = entry.getEndTime()
        currentDateTime = startDateTime
        entry_removed = False

        while currentDateTime < endDateTime:
            entryFile = self.get_entry_file_path(currentDateTime)
            if os.path.exists(entryFile):
                with open(entryFile, 'r') as file:
                    data = json.load(file)

                for i in range(len(data["entries"])):
                    if (data["entries"][i]["activity"] == entry.getActivityName() and
                        data["entries"][i]["start"] == str(entry.getStartTime()) and
                            data["entries"][i]["end"] == str(entry.getEndTime())):
                        del data["entries"][i]
                        entry_removed = True
                        self.update_stats(data, entry, entry.getDuration())
                        break

                if entry_removed:
                    # update the stats here as needed
                    with open(entryFile, 'w') as file:
                        json.dump(data, file, indent=2)
                    break

            currentDateTime += datetime.timedelta(days=1)

        if not entry_removed:
            print(f"Entry {entry.getActivityName()} not found.")

    def checkOverlap(self, new_entry, existing_entries):
        new_start = datetime.datetime.strptime(
            new_entry['start'], '%Y-%m-%d %H:%M:%S')
        new_end = datetime.datetime.strptime(
            new_entry['end'], '%Y-%m-%d %H:%M:%S')

        for entry in existing_entries:
            existing_start = datetime.datetime.strptime(
                entry['start'], '%Y-%m-%d %H:%M:%S')
            existing_end = datetime.datetime.strptime(
                entry['end'], '%Y-%m-%d %H:%M:%S')

            # Check for overlap
            if (new_start < existing_end) and (existing_start < new_end):
                return True
        return False

    def getEntryFilePath(self, currentDateTime):
        entryDirectory = "./data/Entries/"
        return f"{entryDirectory}{currentDateTime.strftime('%Y-%m-%d')}.json"

    def createEntryData(self, entry, startDateTime, endDateTime, duration):
        return {
            "activity": entry.getActivityName(),
            "start": str(startDateTime),
            "end": str(endDateTime),
            "duration": str(duration)
        }

    def loadOrCreateData(self, entryFile, entryData):
        if os.path.exists(entryFile):
            with open(entryFile, 'r') as file:
                data = json.load(file)
            data["entries"].append(entryData)
        else:
            data = {"entries": [entryData], "stats": self.initialize_stats()}
        return data

    def initializeStats(self):
        return {
            "totalActivities": 0,
            "totalDuration": "00:00:00",
            "uniqueActivities": [],
            "activityCounts": {},
            "activityDurations": {}
        }

    def updateStats(self, entryFile):
        pass

    def saveToFile(self, entryFile, data):
        with open(entryFile, 'w') as file:
            json.dump(data, file, indent=2)

    def showActivities(self):
        with open(self.activitiesJSON, 'r') as file:
            data = json.load(file)

        for item in data["activities"]:
            print("Activity: " + colored(item['activity'], item['color']))
