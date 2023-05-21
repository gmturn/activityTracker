from Models.EntryModel import Entry
import datetime
import EntryManager

startDateTime = datetime.datetime(2002, 10, 28, 16, 0, 0)
endDateTime = datetime.datetime(2002, 10, 28, 19, 30, 0)


myEntry2 = Entry("Weight Lifting", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()

myManager.addEntry(myEntry2)
