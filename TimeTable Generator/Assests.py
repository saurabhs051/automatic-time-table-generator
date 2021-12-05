import numpy as np

#-----------------------------------------------------------------------------------
#    Constraint Class
#-----------------------------------------------------------------------------------
class constraints:
    def __init__(self):
        self.__continous = 0
        self.__maxClassesToAllot = 5

    def getContinousClasses(self):
        return self.__continous
    def getMaxClassesToAllot(self):
        return self.__maxClassesToAllot
    def setContinousClasses(self,continous):
        self.__continous = continous
    def setMaxClassesToAllot(self,maximumClassToAllot):
        self.__maxClassesToAllot = maximumClassToAllot

         
    

#-----------------------------------------------------------------------------------
#    Subject Class
#-----------------------------------------------------------------------------------

class subjects:

#subjects s(cs-08,DSA,4)
    def __init__(self,subID = None,subName = None,subCreditsorLoads = None):
       self.__ID = subID
       self.__Name = subName
       self.__CreditsorLoads = int(subCreditsorLoads)

## Getters and Setters

    ##Setters
    def setID(self,subID):
        self.__ID = subID
    def setName(self,subName):
        self.__Name = subName
    def setCreditsorLoads(self,subCreditsorLoads):
        self.__CreditsorLoads = subCreditsorLoads
    def decreaseCreditsorLoads(self):
        self.__CreditsorLoads -= 1

        

    ##Getters
    def getID(self):
        return self.__ID
    def getName(self):
        return self.__Name
    def getCreditsorLoads(self):
        return self.__CreditsorLoads

#Methods
    def inputSubjects(self):
        self.setID(input('Enter Subject ID : '))
        self.setName(input('Enter Subject Name : '))
        self.setCredits(input('Enter Subject Credit : '))
#--------------------------------------------------------------------------------------
# LAB class uses properties of Suject class
#--------------------------------------------------------------------------------------
class labs(subjects):
    def __init__(self,labName=None,labCredits = 3):
        subjects.__init__(self,subName = labName,subCreditsorLoads = labCredits)
#--------------------------------------------------------------------------------------
# Entities have common properties of TeacherTimeTable and SectionTimeTable
#--------------------------------------------------------------------------------------
class entities:
    def __init__(self,ID,name,subjects,labs):
        self.__ID = ID
        self.__name = name
        self.__subjects = subjects
        self.__labs = labs

#Getters and Setters
    #Getters
    def getID(self):
        return self.__ID
    def getName(self):
        return self.__name
    def getSubjects(self):
        return self.__subjects
    def getLabs(self):
        return self.__labs
    def getTotalCredits(self):
        totalCredits = 0
        for sub in self.__subjects:
            totalCredits += sub.getCreditsorLoads()
        return totalCredits

    #Setters
    def setID(self,ID):
        self.__ID = ID
    def setName(self,Name):
        self.__name = Name
    def setSubjects(self,subjects):
        self.__subjects = subjects
    def setLabs(self,labs):
        self.__labs = labs


#-----------------------------------------------------------------------------------------
#Rooms to be alloted to section to be used in assignment of no classes
#-----------------------------------------------------------------------------------------
class roomEntity:
    def __init__(self, id, campusID, Department, building, roomName, capacity):
        self.__roomID = id
        self.__roomName = roomName
        self.__building = building
        self.__Department = Department
        self.__campusID = campusID
        self.__capacity = capacity
        self.__roomAllSlots = [['*','*','*'], ['*','*','*'], ['*','*','*'],['*','*','*'], ['*','*','*']]
        self.__allottedSlots = 0
##Getters and Setters
    #Setters
    def setRoomCapacity(self,capacity):
        self.__capacity = capacity
    def setRoomName(self,roomName):
        self.__roomName = roomName
    def setBuilding(self,building):
        self.__roomID = building
    def setDepartment(self,Department):
        self.__Department = Department
    def setCampusID(self,campusID):
        self.__campusID = campusID
    def setAllotted(self, day, slot, sectionName):
        print('Before : Day = ' + str(day) + " Slot = " + str(slot))
        print(self.__roomAllSlots)
        self.__roomAllSlots[day][slot] = str(sectionName)
        print('After : ')
        print(self.__roomAllSlots)
    def incrementAllottedSlots(self):
        self.__allottedSlots+=1

    #Getters
    def getRoomID(self):
        return self.__roomID
    def getRoomCapacity(self):
        return self.__capacity
    def getRoomName(self):
        return self.__roomName
    def getBuilding(self):
        return self.__building
    def getDepartment(self):
        return self.__Department
    def getCampusID(self):
        return self.__campusID
    def isAllotted(self, day, slot):
        return self.__roomAllSlots[day][slot] != '*'
    def allottedSlotsCount(self):
        return self.__allottedSlots
    def getAllottedSection(self,day,slot):
        return self.__roomAllSlots[day][slot]
#----------------------------------------------------------------------------------------
# TimeTable has properties which are generic to both (teacher and section) timetable
#----------------------------------------------------------------------------------------
class timetable:
    def __init__(self):
        self.__days = 5
        self.__periods = 9
        self.__timeTable = np.zeros((self.__days,self.__periods),dtype = 'S20')
        self.__all_slots = np.zeros((self.__days,self.__periods),dtype = 'int32')
        self.__roomsAlloted = [['*','*','*','*','*'], ['*','*','*','*','*'], ['*','*','*','*','*'] ]
        
#Getters and Setters
    def getTimeTable(self):
        return self.__timeTable
    def getTimeTableforDay(self,day):
        return self.__timeTable[day]
    def getAllSlots(self):
        return self.__all_slots
    def getDays(self):
        return self.__days
    def getPeriods(self):
        return self.__periods
    def getValidSlots(self,day):        # Valid slot if all 3 periods in that slot is empty
        return [slot for slot in range(3) if self.__all_slots[day][slot] == 0]

    def isfull(self,day,slot):
        return self.__all_slots[day][slot] == 3

    def getFilled(self,day,slot):
        return self.__all_slots[day][slot]

    def addRooms(self, rooms):
        # Unallot room if no subject in that slot

        for day in range(5):
            for emptySlot in self.getValidSlots(day):
                if self.__roomsAlloted[emptySlot][day] != '*':
                    roomName = self.__roomsAlloted[emptySlot][day]
                    self.__roomsAlloted[emptySlot][day] = '*'
                    for room in rooms:
                        if room.getRoomName() == roomName:
                            room.setAllotted(day, emptySlot, '*')
                            break

        for i in range(3):
            self.__timeTable = np.insert(self.__timeTable,i*4,self.__roomsAlloted[i],axis = 1)
        #print(self.__timeTable)

    def setTimeTable(self,timeTable):
        self.__timeTable = timeTable
    def setAllSlots(self,allSlots):
        self.__all_slots = allSlots
#Method
    def updateTimeTable(self,row,col,value):
        self.__timeTable[row][col] = value

    def incrementAllSlotsby(self,row,col,value):
        self.__all_slots[row][col] += value

    def isEmptySlot(self,day,col):
        if self.__all_slots[day][col] != 3: return True
        return False

    def isEmpty(self,day,slot):
        if self.__timeTable[day][slot] == b'':
            return True
        return False

    def meetsConstraints(self,day,period,continous):
        if continous == 0:
            if period != 0 and period != self.__periods-1:
                if self.__timeTable[day][period-1] == b'' and self.__timeTable[day][period+1] == b'':
                    return True
            elif period == 0:
                if self.__timeTable[day][period+1] == b'':
                    return True
            elif self.__timeTable[day][period-1] == b'':
                return True
        return False

    def updateRoomsAllotted(self, day, slot, roomName):
        self.__roomsAlloted[slot][day] = roomName

if __name__ == "__main__":
    pass



    
