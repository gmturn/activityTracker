import json
from colorama import init
from termcolor import colored


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
