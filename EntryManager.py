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

    def removeActivity(self, activityName):
        with open(self.activitiesJSON, 'r') as file:
            data = json.load(file)

         # Filter the "activities" list to remove the specified activity
        try:
            data["activities"] = [activity for activity in data['activities']
                                  if activity['activity'] != activityName]
        except:
            print(f"Error: Could not remove {activityName}. Does not exist.")

        # Open the file in write mode and write the updated JSON data
        with open(self.activitiesJSON, 'w') as file:
            # indent parameter is used to make the output easy to read
            json.dump(data, file, indent=2)

    def showActivities(self):
        with open(self.activitiesJSON, 'r') as file:
            data = json.load(file)

        for item in data["activities"]:
            print("Activity: " + colored(item['activity'], item['color']))

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
            data = self.update_stats(data, entry, duration)
            self.save_to_file(entryFile, data)
            currentDateTime += datetime.timedelta(days=1)

    def get_end_of_day_or_entry(self, currentDateTime, endDateTime):
        return min(currentDateTime.replace(hour=23, minute=59, second=59, microsecond=999999), endDateTime)

    def get_entry_file_path(self, currentDateTime):
        entryDirectory = "./data/Entries/"
        return f"{entryDirectory}{currentDateTime.strftime('%Y-%m-%d')}.json"

    def create_entry_data(self, entry, startDateTime, endDateTime, duration):
        return {
            "activity": entry.getActivityName(),
            "start": str(startDateTime),
            "end": str(endDateTime),
            "duration": str(duration)
        }

    def load_or_create_data(self, entryFile, entryData):
        if os.path.exists(entryFile):
            with open(entryFile, 'r') as file:
                data = json.load(file)
            data["entries"].append(entryData)
        else:
            data = {"entries": [entryData], "stats": self.initialize_stats()}
        return data

    def initialize_stats(self):
        return {
            "totalActivities": 0,
            "totalDuration": "00:00:00",
            "uniqueActivities": [],
            "activityCounts": {},
            "activityDurations": {}
        }

    def update_stats(self, data, entry, duration):
        data["stats"]["totalActivities"] += 1
        # You can create methods to update the total duration and activity data
        data["stats"]["totalDuration"] = self.update_total_duration(
            data["stats"]["totalDuration"], duration)
        data["stats"] = self.update_activity_data(
            data["stats"], entry.getActivityName(), duration)
        return data

    def save_to_file(self, entryFile, data):
        with open(entryFile, 'w') as file:
            json.dump(data, file, indent=2)

    def update_total_duration(self, totalDuration, duration):
        # totalDuration is a string in the format "HH:MM:SS"
        total_seconds = datetime.timedelta(hours=int(totalDuration.split(':')[0]),
                                           minutes=int(
                                               totalDuration.split(':')[1]),
                                           seconds=int(totalDuration.split(':')[2])).total_seconds()
        total_seconds += duration.total_seconds()
        updated_duration = datetime.timedelta(seconds=total_seconds)

        # Convert updated_duration back to "HH:MM:SS" format
        hours, remainder = divmod(updated_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_activity_data(self, stats, activityName, duration):
        if activityName not in stats["uniqueActivities"]:
            stats["uniqueActivities"].append(activityName)
            stats["activityCounts"][activityName] = 1
            stats["activityDurations"][activityName] = str(duration)
        else:
            stats["activityCounts"][activityName] += 1
            current_activity_duration = stats["activityDurations"][activityName]
            updated_activity_duration = self.update_total_duration(
                current_activity_duration, duration)
            stats["activityDurations"][activityName] = updated_activity_duration
        return stats
