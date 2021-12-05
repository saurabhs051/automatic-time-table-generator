from Assests import entities,timetable,constraints,np

#-----------------------------------------------------------------------------
#Section timeTable
#-----------------------------------------------------------------------------

class sectionTimeTable(entities,timetable):
    def __init__(self,sectionID = '',sectionName = '',branch = '',semester='',subjects = [],labs = []):
        entities.__init__(self,sectionID,sectionName,subjects,labs)
        timetable.__init__(self)
        self.__teachersAlloted = {}
        namesSem = ['st Sem', 'nd Sem', 'rd Sem', 'th Sem', 'th Sem', 'th Sem', 'th Sem', 'th Sem']
        self.__semester = semester + namesSem[int(semester)-1]
        self.__branch = branch

#Getters and Setters
    #Getters

    def getSemester(self):
        return self.__semester

    def setSemester(self,sem):
        self.__semester = sem

    def getBranch(self):
        return self.__branch
    
    def getTeachersAlloted(self):
        return self.__teachersAlloted

    def getTeacherAllotedforSubject(self,subject):
        return self.__teachersAlloted[subject]

    def getCredits(self,sub):
        return sub.getCreditsorLoads()
    #Setters
    def setTeachersAlloted(self,teachersAlloted):
        self.__teachersAlloted = teachersAlloted

#Method
    def addTeacherforSubject(self,subject,teacher):
        self.__teachersAlloted[subject] = teacher

#getTotalSubkect credit
    def enoughSlots(self):
        totalCredits = self.getTotalCredits()
        remainingSlots = self.getDays()*self.getPeriods() - (3*self.getDays()+3*len(self.getLabs()))
        if totalCredits > remainingSlots:
            return False
        return True

    def decreaseCredits(self,subject):
        subject.decreaseCreditsorLoads()

    #Allot rooms to empty(yet to be allotted) slots of each day
    def assignRooms(self, rooms):
        for day in range(5):
            validSlots = self.getValidSlots(day)
            for slot in validSlots:
                for room in rooms:
                    if room.allottedSlotsCount() == 3:      # Room full throughout the day
                        continue
                    if not room.isAllotted(day, slot):      # Required slot available in the room
                        room.setAllotted(day, slot, self.getName())
                        self.updateRoomsAllotted(day, slot, room.getRoomName())
                        break



#assigning no classes **(can be used for room assignment)
    def assignNoClasses(self):
        randSlots = np.random.randint(low=1,high=4,size = 5)
        for i in range(5):
            if randSlots[i] == 1:
                self.updateTimeTable(i,0,'No Class')
                self.updateTimeTable(i,1,'No Class')
                self.updateTimeTable(i,2,'No Class')
                self.incrementAllSlotsby(i,0,3)
            elif randSlots[i] == 2:
                self.updateTimeTable(i,3,'No Class')
                self.updateTimeTable(i,4,'No Class')
                self.updateTimeTable(i,5,'No Class')
                self.incrementAllSlotsby(i,1,3)
            else:
                self.updateTimeTable(i,6,'No Class')
                self.updateTimeTable(i,7,'No Class')
                self.updateTimeTable(i,8,'No Class')
                self.incrementAllSlotsby(i,2,3)

#assigning labs
    def assignLabs(self):
        count = 0
        days = [0]*5
        secLabs = self.getLabs()
        while(count < len(secLabs)):
            day = np.random.randint(0,5)
            slot = np.random.randint(0,3)
            if self.isEmptySlot(day,slot) and days[day] != 1:
                days[day] = 1
                self.updateTimeTable(day,0 + 3*slot,secLabs[count].getName())
                self.updateTimeTable(day,1 + 3*slot,secLabs[count].getName())
                self.updateTimeTable(day,2 + 3*slot,secLabs[count].getName())
                self.incrementAllSlotsby(day,slot,3)
                count += 1




#---------------------------------------------------------------------------#
#Teacher TimeTable
#---------------------------------------------------------------------------#

class teacherTimeTable(entities,timetable,constraints):
    def __init__(self,teacherID = None,teacherName=None,subjects = [],labs = []):
        entities.__init__(self,teacherID,teacherName,subjects,labs)
        constraints.__init__(self)
        timetable.__init__(self)
        self.__classesAlloted = 0
        self.__sectionAlloted = {} #{'DSA' : 'CS-5'} a dictionary.!
        self.__canAssignSec = True
#Getters and Setters
    #Getters
    def getNumClassesAlloted(self):
        return self.__classesAlloted
    def getSectionAlloted(self):
        return self.__sectionAlloted
    def getCanAssignSec(self):
        return self.__canAssignSec
    def getSubjectforSection(self,section):
        return self.__sectionAlloted[section]
    def getLoad(self,subject):
        return subject.getCreditsorLoads()
    #Setters
    def setNumClassesAlloted(self,classesAlloted):
        self.__classesAlloted = classesAlloted
    def setSectionAlloted(self,sectionAlloted):
        self.__sectionAlloted = sectionAlloted
    def setCanAssignSec(self,val):
        self.__canAssignSec = val
    def updateSubjectLoad(self,subject):
        subject.decreaseCreditsorLoads()
##        for sub in self.getSubjects():
##            if subject is sub:
##                sub.decreaseCreditsorLoads()
##                break

    def check(self,i,j,name):
        if self.isEmpty(i,j) and self.meetsConstraints(i,j,self.getContinousClasses()):
            self.updateTimeTable(i,j,name)
            return True
        return False


##Methods
    #method to check if section exists or not in teacher's Bag.!
    def checkSectionExistance(self,sec):
        if sec in self.__sectionAlloted.values():
            return True
        return False
       
     #after allotation of each class
    def incrementClassesAlloted(self):
        self.__classesAlloted += 1
    def addSectionforSubject(self,subject,section):
        self.__sectionAlloted[subject] = section

        
if __name__ == '__main__':
    pass
##    t = teacherTimeTable()
##    t.setSectionAlloted({'DSA':'CS-5'})
##    print(t.checkSectionExistance('CS-6'))
##    print(t.getTimeTable())
##    t.updateTimeTable(3,5,1123)
##    print(t.getTimeTable())








        
    
    
