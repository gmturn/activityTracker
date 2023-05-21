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
                raise ValueError(
                    f"Error: An activity with the name '{activity}' already exists.")

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

            data = self.loadOrCreateData(entryFile)

            if self.checkOverlap(entryData, data["entries"]):
                raise ValueError("Error: Overlapping entry.")

            data["entries"].append(entryData)  # data is correctly initialized

            data["stats"] = self.updateStats(data, entry, "add")
            self.saveToFile(entryFile, data)
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
            entryFile = self.getEntryFilePath(currentDateTime)
            if os.path.exists(entryFile):
                with open(entryFile, 'r') as file:
                    data = json.load(file)

                for i in range(len(data["entries"])):
                    if (data["entries"][i]["activity"] == entry.getActivityName() and
                        data["entries"][i]["start"] == str(entry.getStartTime()) and
                            data["entries"][i]["end"] == str(entry.getEndTime())):
                        del data["entries"][i]
                        entry_removed = True
                        self.updateStats(entry, entry.getDuration())
                        break

                if entry_removed:
                    # update the stats here as needed
                    with open(entryFile, 'w') as file:
                        json.dump(data, file, indent=2)
                    break

            currentDateTime += datetime.timedelta(days=1)

        if not entry_removed:
            raise ValueError(f"Entry {entry.getActivityName()} not found.")

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

    def loadOrCreateData(self, entryFile):
        if os.path.exists(entryFile):
            with open(entryFile, 'r') as file:
                data = json.load(file)
        else:
            data = {"entries": [], "stats": self.initializeStats()}
        return data

    def initializeStats(self):
        return {
            "totalActivities": 0,
            "totalDuration": "00:00:00",
            "uniqueActivities": [],
            "activityCounts": {},
            "activityDurations": {}
        }

    def updateStats(self, data, entry, operation):
        if not isinstance(entry, Entry):
            raise ValueError(
                "Error: updateStats was passed an invalid Entry data type")

        totalActivities = self.updateTotalActivities(data)
        totalDuration = self.updateTotalDuration(data)
        uniqueActivities = self.updateUniqueActivities(data)
        activityCounts = self.updateActivityCounts(data)
        activityDurations = self.updateActivityDurations(data)

        stats = {"totalActivities": totalActivities,
                 "totalDuration": totalDuration,
                 "uniqueActivities": uniqueActivities,
                 "activityCounts": activityCounts,
                 "activityDurations": activityDurations
                 }
        return stats

    def updateTotalActivities(self, data):
        numActivities = 0
        for entry in data["entries"]:
            numActivities += 1
        return numActivities

    def updateTotalDuration(self, data):
        totalDuration = datetime.timedelta()

        for entry in data["entries"]:
            time_object = datetime.datetime.strptime(
                entry["duration"], "%H:%M:%S")
            duration = time_object - \
                datetime.datetime.strptime("00:00:00", "%H:%M:%S")
            totalDuration += duration

        # Format timedelta as a string
        total_duration_str = str(totalDuration)

        return total_duration_str

    def updateUniqueActivities(self, data):
        uniqueActivities = []
        for entry in data["entries"]:
            if entry["activity"] not in uniqueActivities:
                uniqueActivities.append(entry["activity"])

        return uniqueActivities

    def updateActivityCounts(self, data):
        activityCounts = {}
        for entry in data["entries"]:
            if entry["activity"] not in activityCounts:
                activityCounts[entry["activity"]] = 1

            else:
                activityCounts[entry["activity"]] += 1

        return activityCounts

    def updateActivityDurations(self, data):
        activityDurations = {}
        for entry in data["entries"]:
            if entry["activity"] not in activityDurations:
                activityDurations[entry["activity"]] = entry["duration"]
            else:
                current_duration = datetime.datetime.strptime(
                    activityDurations[entry["activity"]], "%H:%M:%S") - datetime.datetime.strptime("00:00:00", "%H:%M:%S")
                new_duration = datetime.datetime.strptime(
                    entry["duration"], "%H:%M:%S") - datetime.datetime.strptime("00:00:00", "%H:%M:%S")
                total_duration = current_duration + new_duration
                # convert timedelta object to string in format "HH:MM:SS"
                activityDurations[entry["activity"]] = str(total_duration)
        return activityDurations

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
