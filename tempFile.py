from Models.EntryModel import Entry
import datetime

startDateTime = datetime.datetime(2002, 10, 28, 22, 29, 0)
endDateTime = datetime.datetime(2002, 10, 30, 0, 4, 0)


myEntry = Entry("Muay Thai", startDateTime, endDateTime)

print(myEntry)
