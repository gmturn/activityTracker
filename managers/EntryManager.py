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
        data = self.loadActivities()

        if self.activityExists(activity, data):
            raise ValueError(
                f"Error: An activity with the name '{activity}' already exists.")

        data['activities'].append({"activity": activity, "color": color})
        self.saveActivities(data)

    def removeActivity(self, activity):
        data = self.loadActivities()

        if not self.activityExists(activity, data):
            raise ValueError(
                f"Error: No activity with the name '{activity}' found.")

        data['activities'] = [a for a in data['activities']
                              if a['activity'] != activity]
        self.saveActivities(data)

    def loadActivities(self):
        with open(self.activitiesJSON, 'r') as file:
            return json.load(file)

    def getActivityList(self):
        data = self.loadActivities()
        activities = []
        for activity in data["activities"]:
            activities.append(activity["activity"])
        return activities

    def saveActivities(self, data):
        with open(self.activitiesJSON, 'w') as file:
            json.dump(data, file, indent=2)

    def activityExists(self, activity, data):
        for existing_activity in data['activities']:
            if existing_activity['activity'] == activity:
                return True
        return False

    def addEntry(self, entry):
        if not isinstance(entry, Entry):
            raise ValueError(
                "Error: EntryManager.addEntry(entry) value is not type Entry.")

        startDateTime = entry.getStartTime()
        endDateTime = entry.getEndTime()

        if startDateTime > endDateTime:
            raise ValueError(
                "Error: Start time cannot be later than end time.")

        currentDateTime = startDateTime
        while currentDateTime.date() < endDateTime.date() or currentDateTime.time() < endDateTime.time():
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

            data["stats"] = self.updateStats(data, entry)
            self.saveToFile(entryFile, data)
            currentDateTime = nextDateTime + datetime.timedelta(seconds=1)

    def removeEntry(self, entry):
        if not isinstance(entry, Entry):
            raise ValueError(
                "Error: EntryManager.removeEntry(entry) value is not type Entry.")

        startDateTime = entry.getStartTime()
        endDateTime = entry.getEndTime()
        currentDateTime = startDateTime

        if startDateTime > endDateTime:
            raise ValueError(
                "Error: Start time cannot be later than end time.")

        while currentDateTime < endDateTime:
            nextDateTime = self.getEndOfDayOrEntry(
                currentDateTime, endDateTime)

            duration = nextDateTime - currentDateTime
            entryFile = self.getEntryFilePath(currentDateTime)

            entryData = self.createEntryData(
                entry, currentDateTime, nextDateTime, duration)

            data = self.loadOrCreateData(entryFile)

            if entryData not in data["entries"]:
                raise ValueError("Error: Entry not found.")

            data["entries"].remove(entryData)

            data["stats"] = self.updateStats(data, entry)
            self.saveToFile(entryFile, data)

            currentDateTime += datetime.timedelta(days=1)

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

    def updateStats(self, data, entry):
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
        end_of_current_day = currentDateTime.replace(
            hour=23, minute=59, second=59)

        if endDateTime.date() > currentDateTime.date():
            # If endDateTime is on a different day, then return end of the current day
            return end_of_current_day
        else:
            # If endDateTime is on the same day, then return the actual end time
            return min(end_of_current_day, endDateTime)
