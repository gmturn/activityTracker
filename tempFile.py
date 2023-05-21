from Models.EntryModel import Entry
import datetime
import EntryManager

startDateTime = datetime.datetime(2023, 5, 20, 9, 0, 0)
endDateTime = datetime.datetime(2023, 5, 20, 11, 30, 0)


myEntry2 = Entry("Weight Lifting", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()

data = myManager.addEntry(myEntry2)
