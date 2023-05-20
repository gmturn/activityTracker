from Models.EntryModel import Entry
import datetime
import EntryManager

startDateTime = datetime.datetime(2002, 10, 28, 22, 29, 0)
endDateTime = datetime.datetime(2002, 10, 30, 0, 4, 0)


myEntry = Entry("Muay Thai", startDateTime, endDateTime)
myEntry2 = Entry("Running", startDateTime, endDateTime)


myManager = EntryManager.EntryManager()
myManager.removeActivity("Activity 1")
myManager.removeActivity("Activity 2")


myManager.addActivity("Muay Thai", "red")
myManager.addActivity("Running", "green")
myManager.addActivity("Bad Activity", "black")

myManager.showActivities()
