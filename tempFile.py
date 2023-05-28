from Models.EntryModel import Entry
import datetime
import managers.EntryManager as EntryManager

startDateTime = datetime.datetime(2023, 5, 27, 11, 0, 0)
endDateTime = datetime.datetime(2023, 5, 27, 13, 30, 0)


myEntry2 = Entry("Weight Lifting", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()
