import datetime


class Entry:
    def __init__(self, activityName, startDateTime, endDateTime):
        if type(activityName) == str and isinstance(startDateTime, datetime.datetime) and isinstance(endDateTime, datetime.datetime):
            self.activityName = activityName
            self.startDateTime = startDateTime
            self.endDateTime = endDateTime
            self.duration = self.calcDuration()

        else:
            raise ValueError(
                "Error: Type activityName, date, startDateTime or endDateTime not valid.")

    def calcDuration(self):
        totalDuration = self.endDateTime - self.startDateTime
        return totalDuration

    def __str__(self):
        completeEntry = f"""{self.activityName}
Start Time: {self.startDateTime}
End Time: {self.endDateTime}
Total Duration: {self.duration}
"""
        return completeEntry

    def setStartTime(self, startDateTime):
        self.startDateTime = startDateTime

    def setEndTime(self, endDateTime):
        self.endDateTime = endDateTime

    def getStartTime(self):
        return self.startDateTime

    def getEndTIme(self):
        return self.endDateTime
