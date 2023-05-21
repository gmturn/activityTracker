from Models.EntryModel import Entry
import datetime
import EntryManager

startDateTime = datetime.datetime(2023, 5, 20, 12, 0, 0)
endDateTime = datetime.datetime(2023, 5, 20, 13, 30, 0)


# myEntry = Entry("Weight Lifting", startDateTime, endDateTime)
myEntry2 = Entry("Weight Lifting", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()
myManager.removeEntry(myEntry2)
