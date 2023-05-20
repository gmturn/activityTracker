from datetime import datetime


class Entry:
    def __init__(self, activityName, day, startTime, endTime):
        self.activityName = activityName
        self.day = day
        self.startTime = startTime
        self.endTime = endTime
