from Models.EntryModel import Entry
import datetime
import EntryManager

startDateTime = datetime.datetime(2023, 5, 20, 12, 0, 0)
endDateTime = datetime.datetime(2023, 5, 20, 13, 15, 0)


myEntry = Entry("Weight Lifting", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()
