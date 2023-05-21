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

        while currentDateTime < endDateTime:  # loops continuously if entry lasts over the span of multiple days
            nextDateTime = self.getEndOfDayOrEntry(
                currentDateTime, endDateTime)

            duration = nextDateTime - currentDateTime
            entryFile = self.getEntryFilePath(currentDateTime)

            entryData = self.createEntryData(
                entry, currentDateTime, nextDateTime, duration)

            data = self.loadOrCreateData(entryFile, entryData)

            if self.checkOverlap(entryData, data["entries"]):
                raise ValueError("Error: Overlapping entry.")

            data = self.updateStats(data, entry, duration, "add")
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

    def updateStats(self, data, entry, duration, operation):
        activity = entry.getActivityName()
        durationStr = str(duration)
        
        # initialize the stats if they don't exist
        if "stats" not in data:
            data["stats"] = {
                "totalDuration": "0:00:00",
                "uniqueActivities": [],
                "activityCounts": {},
                "activityDurations": {}
            }
    
        # parse total duration and new duration as timedelta
        totalDuration = datetime.datetime.strptime(data["stats"]["totalDuration"], "%H:%M:%S") - datetime.datetime(1900, 1, 1)
        newDuration = datetime.datetime.strptime(durationStr, "%H:%M:%S") - datetime.datetime(1900, 1, 1)
    
        # update total duration
        if operation == "add":
            totalDuration += newDuration
        elif operation == "remove":
            totalDuration -= newDuration
    
        # update total duration string in stats
        data["stats"]["totalDuration"] = str(totalDuration)
    
        # update unique activities
        if activity not in data["stats"]["uniqueActivities"]:
            data["stats"]["uniqueActivities"].append(activity)
        
        # update activity counts and durations
        if activity not in data["stats"]["activityCounts"]:
            if operation == "add":
                data["stats"]["activityCounts"][activity] = 1
                data["stats"]["activityDurations"][activity] = durationStr
            elif operation == "remove":
                print("Error: Trying to remove activity that does not exist.")
                return data
        else:
            if operation == "add":
                data["stats"]["activityCounts"][activity] += 1
                activityDuration = datetime.datetime.strptime(data["stats"]["activityDurations"][activity], "%H:%M:%S") - datetime.datetime(1900, 1, 1)
                activityDuration += newDuration
                data["stats"]["activityDurations"][activity] = str(activityDuration)
            elif operation == "remove":
                data["stats"]["activityCounts"][activity] -= 1
                if data["stats"]["activityCounts"][activity] == 0:
                    del data["stats"]["activityCounts"][activity]
                    del data["stats"]["activityDurations"][activity]


    def saveToFile(self, entryFile, data):
        with open(entryFile, 'w') as file:
            json.dump(data, file, indent=2)

    def showActivities(self):
        with open(self.activitiesJSON, 'r') as file:
            data = json.load(file)

        for item in data["activities"]:
            print("Activity: " + colored(item['activity'], item['color']))

    def getEndOfDayOrEntry(self, currentDateTime, endDateTime):
        return min(currentDateTime.replace(hour=23, minute=59, second=59, microsecond=999999), endDateTime)
