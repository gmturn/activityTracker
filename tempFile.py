from Models.EntryModel import Entry
import datetime
import managers.EntryManager as EntryManager

startDateTime = datetime.datetime(2023, 5, 28, 2, 0, 0)
endDateTime = datetime.datetime(2023, 5, 28, 4, 30, 0)


myEntry2 = Entry("Coding", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()
