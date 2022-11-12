import sys
from entities_objectives import *

roomCoorD = {}  # a dictionary with all the rooms and their coordinates, populated by room(__init__)

def list2tuple(x):
    return tuple(x)

def str_to_class(txt):
    return getattr(sys.modules[__name__], txt)

def roomFromCoor(coor):
    roomCoorKeys = list(roomCoorD.keys())
    roomCoorVals = list(roomCoorD.values())
    position = roomCoorKeys.index(list2tuple(coor))
    currentRoom = str_to_class(roomCoorVals[position])
    return currentRoom

class Room:
    def __init__(self,name,coor,shortT,longT,lookL,exitsL,synonyms,
                 subject1={},subject2={},lookAtT="",locked=False,useL=[],askL=[],takeD={}):
        self.name = name
        self.coor = coor
        self.shortT = shortT
        self.longT = longT
        self.lookL = lookL
        self.lookAtT = lookAtT
        self.locked = locked
        self.useL = useL
        self.askL = askL
        self.subject1 = subject1
        self.subject2 = subject2
        self.takeD = takeD
        self.exitsL = exitsL
        self.synonyms = synonyms
        self.synonyms.append(self.name)
        roomCoorD[self.coor] = self.name
        synonymsD[self.name] = self.synonyms

    def checkIfPresent(self,ele,rList):
        return True if ele in rList else False

    def look(self):
        print(self.longT)
        if self.takeD:
            [print(values) for values in self.takeD.values()] #if there are valid items, will print description

    def lookAt(self):  # a function for looking at a room from the outside
        print(self.lookAtT)

    def tryEnter(self):
        if self.locked is True:
            print("The door is locked.")
            return False  # cannot enter
        else:
            return True

    def enter(self): #enters the new room, prints the new room's name and looks around
        print(self.shortT)
        print(self.longT)
        return str_to_class(self.name)


class Stairs(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def climbStairsExhaustion(self): #If you climb to many stairs, you will become tired
        player.nStairsClimbed+=1
        if player.nStairsClimbed > 2:
            manyStairsClimbed.complete(player.nStairsClimbed)


class Hallway(Room):
    def __init__(self,name,coor,exitsL,synonyms,takeD={},
                 lookL=[],askL=[],useL=["key"], shortT = "You are in a hallway.", longT="",
                 locked=False):
        self.name = name
        self.coor = coor
        self.classroomNumber = self.name[-3:]
        self.useL = useL
        self.askL = askL
        self.lookL = lookL
        self.shortT = shortT
        self.longT = longT
        self.exitsL = exitsL
        self.locked = locked
        self.takeD = takeD
        self.synonyms = synonyms
        self.synonyms.append(self.name)
        roomCoorD[self.coor] = self.name
        synonymsD[self.name] = self.synonyms


        if self.name.endswith("1"):
            self.longT=f"To your north is classroom {self.classroomNumber}.\n" \
                       f"To your east is the hall section with the stairs.\n" \
                       f"The hallway continues to your west."
        elif self.name.endswith("2"):
            self.longT=f"To your north is classroom {self.classroomNumber}.\n" \
                  f"The hallway continues to your east and to your west."
        elif self.name.endswith("3"):
            self.longT=f"To your north is classroom {self.classroomNumber}.\n" \
                  f"This is the end of the hallway. You can go back east."
        elif self.name.endswith("4"):
            self.longT=f"To your east is classroom {self.classroomNumber}.\n" \
                  f"To your north is the hall section with the stairs.\n" \
                  f"The hallway continues to your south."
        elif self.name.endswith("5"):
            self.longT=f"To your east is classroom {self.classroomNumber}.\n" \
                  f"The hallway continues to your north and to your south."
        elif self.name.endswith("6"):
            self.longT=f"To your east is classroom {self.classroomNumber}.\n" \
                  f"This is the end of the hallway. You can go back north."


class lockedRoom(Room):
    def __init__(self,coor,name,synonyms,useL=[],askL=[],takeD={},shortT="",longT="",lookL=[],exitsL=[],locked=True,
                 lookAtT="The lights are off - too dark to make anything out..."):
        self.coor = coor
        self.name = name
        self.shortT = shortT
        self.longT = longT
        self.lookL = lookL
        self.exitsL = exitsL
        self.useL = useL
        self.locked = locked
        self.askL = askL
        self.takeD = takeD
        self.lookAtT = lookAtT
        self.synonyms = synonyms
        self.synonyms.append(self.name)
        roomCoorD[self.coor] = self.name
        synonymsD[self.name] = self.synonyms

    def lookAt(self):
        print(f"You peer through the window of room {self.name[-3:]}.")
        print(self.lookAtT)

        #special
        if self.name == "room105" and findBreakRoom.done is False:
            findBreakRoom.complete()

class wrongRoom(Room):
    def __init__(self, coor, name, synonyms, subject1, subject2, useL=["register"], askL=["teacher","student"],
                 takeD={"register":"There's a sheet of paper laying on the table near the door."},
                 shortT="", longT="", lookL=["register","student","register"],
                 exitsL=[],
                 locked=False,
                 lookAtT=""):
        self.coor = coor
        self.name = name
        self.shortT = shortT
        self.longT = longT
        self.lookL = lookL
        self.subject1 = subject1
        self.subject2 = subject2
        self.exitsL = exitsL
        self.useL = useL
        self.locked = locked
        self.askL = askL
        self.takeD = takeD
        self.lookAtT = lookAtT
        self.synonyms = synonyms
        self.synonyms.append(self.name)
        roomCoorD[self.coor] = self.name
        synonymsD[self.name] = self.synonyms
        self.shortT = f"You are in classroom {self.name[-3:]}."
        self.exitsL = ["s"] if self.name.endswith(("1","2","3")) else ["w"]

    def lookAt(self):
        print(f"The door is open and the lights are on. You look inside {self.name[-3:]}.")
        print(self.lookAtT)

#FIRST FLOOR HALLWAYS
hallway101 = Hallway(
    name="hallway101",
    coor=(-1,1,1),
    exitsL=["e","w","n"],
    synonyms=[],
    lookL=["room101"]
)

hallway102 = Hallway(
    name="hallway102",
    coor=(-2,1,1),
    exitsL=["e","w","n"],
    synonyms=[],
    lookL=["room102"]
)

hallway103 = Hallway(
    name="hallway103",
    coor=(-3,1,1),
    exitsL=["e","n"],
    lookL=["room103"],
    synonyms=[]
)

hallway104 = Hallway(
    name="hallway104",
    coor=(0,0,1),
    exitsL=["e","s","n"],
    synonyms=[],
    lookL=["room104"]
)

hallway105 = Hallway(
    name="hallway105",
    coor=(0,-1,1),
    exitsL=["e","s","n"],
    synonyms=[],
    lookL=["room105"]
)

hallway106 = Hallway(
    name="hallway106",
    coor=(0,-2,1),
    exitsL=["e","n"],
    synonyms=[],
    lookL=["room106"]
)

#SECOND FLOOR HALLWAYS
hallway201 = Hallway(
    name="hallway201",
    coor=(-1,1,2),
    exitsL=["e","w","n"],
    synonyms=[],
    lookL=["room201"]
)

hallway202 = Hallway(
    name="hallway202",
    coor=(-2,1,2),
    exitsL=["e","w","n"],
    synonyms=[],
    lookL=["room202"]
)

hallway203 = Hallway(
    name="hallway203",
    coor=(-3,1,2),
    exitsL=["e","n"],
    synonyms=[],
    lookL=["room203"]
)

hallway204 = Hallway(
    name="hallway204",
    coor=(0,0,2),
    exitsL=["e","s","n"],
    synonyms=[],
    lookL=["room204"]
)

hallway205 = Hallway(
    name="hallway205",
    coor=(0,-1,2),
    exitsL=["e","s","n"],
    synonyms=[],
    lookL=["room205"]
)

hallway206 = Hallway(
    name="hallway206",
    coor=(0,-2,2),
    exitsL=["e","n"],
    synonyms=[],
    lookL=["room206"]
)

#THIRD FLOOR HALLWAYS
hallway301 = Hallway(
    name="hallway301",
    coor=(-1,1,3),
    exitsL=["e","w","n"],
    synonyms=[],
    lookL=["room301"]
)

hallway302 = Hallway(
    name="hallway302",
    coor=(-2,1,3),
    exitsL=["e","w","n"],
    synonyms=[],
    lookL=["room302"]
)

hallway303 = Hallway(
    name="hallway303",
    coor=(-3,1,3),
    exitsL=["e","n"],
    synonyms=[],
    lookL=["room303"]
)

hallway304 = Hallway(
    name="hallway304",
    coor=(0,0,3),
    exitsL=["e","s","n"],
    synonyms=[],
    lookL=["room304"]
)

hallway305 = Hallway(
    name="hallway305",
    coor=(0,-1,3),
    exitsL=["e","s","n"],
    synonyms=[],
    lookL=["room305"]
)

hallway306 = Hallway(
    name="hallway306",
    coor=(0,-2,3),
    exitsL=["e","n"],
    synonyms=[],
    lookL=["room306"]
)

lobby = Room(
    name="lobby",
    coor=(0,0,0),
    shortT="You are in the lobby.",
    longT="Someone is manning the reception desk.\n"
          "A massive digital display is hanging up high.\n"
          "To the north is an ascending staircase to the first floor.\n"
          "To the south is the exit of the building.\n"
          "There is a bar to your west.",
    lookL=["receptionist","bar","exit","display"],
    askL=["receptionist"],
    takeD={"pen": "A Syntra-branded pen is laying on the reception desk."},
    exitsL=["n","s","w"],
    synonyms=[]
)

toilets = Room(
    name="toilets",
    coor=(1,1,1),
    shortT= "You enter the lavatory.",
    longT="> You can use the toilets here.\n"
          "To your west is the hallway. It's the only exit.",
    lookL=["toilet"],
    exitsL = ["w"],
    useL=["toilet"],
    synonyms=[]
)

stairs0 = Stairs(
    name="stairs0",
    coor=(0,1,0),
    shortT = "You are in the stairwell on the ground floor.",
    longT = "To your south is the Lobby.\n"
            "The classrooms are upstairs.",
    lookL = [],
    exitsL = ["s","u"],
    synonyms=[]
)

#Stairs objects are folded because they are boring.
stairs1 = Stairs(
    name="stairs1",
    coor=(0,1,1),
    shortT = "You are near the stairs on the first floor.",
    longT = "The hallway to your east leads to the toilets.\n"
            "Classrooms 101-103 are to your west.\n"
            "Classrooms 104-106 are to your south.\n"
            "There are more classrooms upstairs.\n"
            "If you head down you will be in the ground floor stairwell which leads into the lobby.",
    lookL = [],
    exitsL = ["s","e","w","u","d"],
    synonyms=[]
)

stairs2 = Stairs(
    name="stairs2",
    coor=(0,1,2),
    shortT = "You are near the stairs on the second floor.",
    longT = "Classrooms 201-203 are to your west.\n"
            "Classrooms 204-206 are to your south.\n"
            "There are more classrooms upstairs.\n"
            "You can take the steps back down to the first floor.",
    lookL = [],
    exitsL = ["s","w","u","d"],
    synonyms=[]
)

stairs3=Stairs(
    name = "stairs3",
    coor=(0,1,3),
    shortT = "You are near the stairs on the third floor.",
    longT = "This is the top floor.\n"
            "Classrooms 301-303 are to your west.\n"
            "Classrooms 304-306 are to your south.\n"
            "You can take the steps back down to the second floor.",
    lookL=[],
    exitsL = ["s","w","d"],
    synonyms=[]
)

#closed classrooms
room103 = lockedRoom(
    name="room103",
    coor=(-3,2,1),
    synonyms=["103"]
)
room104 = lockedRoom(
    name="room104",
    coor=(1,0,1),
    synonyms=["104"]
)
room105 = lockedRoom(
    name="room105",
    coor=(1,-1,1),
    shortT= "You are in the breakroom.",
    longT= "There's a large aluminium dispenser on the table, as well as several cups.\n"
           "The other student is looking at the dispenser as if they hold a grudge against it.\n"
           "The exit is to your east.",
    lookL= ["dispenser","student"],
    askL=["student"],
    useL=["dispenser"],
    takeD={"cup": "Next to the dispenser are several cups."},
    synonyms=["105"],
    exitsL=["w"],
    lookAtT="The lights are on, but nobody's there.\n"
            "You spot a large, insulated dispenser on one of the tables, alongside some cups."
)
room106 = lockedRoom(
    name="room106",
    coor=(1,-2,1),
    synonyms=["106"]
)
room202 = lockedRoom(
    name="room202",
    coor=(-2,2,2),
    synonyms=["202"]
)
room204 = lockedRoom(
    name="room204",
    coor=(1,0,2),
    synonyms=["204"]
)
room205 = lockedRoom(
    name="room205",
    coor=(1,-1,2),
    synonyms=["205"]
)
room206 = lockedRoom(
    name="room206",
    coor=(1,-2,2),
    synonyms=["206"]
)
room302 = lockedRoom(
    name="room302",
    coor=(-2,2,3),
    synonyms=["302"]
)
room301 = lockedRoom(
    name="room301",
    coor=(-1,2,3),
    synonyms=["301"]
)
room304 = lockedRoom(
    name="room304",
    coor=(1,0,3),
    synonyms=["304"]
)
room306 = lockedRoom(
    name="room306",
    coor=(1,-2,3),
    synonyms=["306"]
)

room102=Room(
    name="room102",
    coor=(-2,2,1),
    synonyms=["102"],
    shortT="You are in classroom 102.",
    askL=["teacher","student"],
    lookL=["teacher","student","key","register"],
    exitsL=["s"],
    subject1={"    ...data type mutability!": 3},
    subject2={"    ...when to use list comprehensions!": 3},
    lookAtT="There's a nerd with a friendly expression writing something on the whiteboard.\n"
            '"Come in, come in!" She beacons you over.',
    longT=f"The exit is to your south.\n"
          "There's a teacher getting ready for class.\n"
          "A student is franticly working on their laptop.\n"
          "> You can [wait] to wait until the lessons start, if you want.",
    takeD={"key":"A key with a comically large keychain is laying on the teacher's desk.",
           "register":"There's a sheet of paper laying on the table near the door."}
)

room101=wrongRoom(  # project management
    name="room101",
    coor=(-1,2,1),
    synonyms=["101"],
    subject1={"    ...how to define milestones and iterations!":3},
    subject2={"    ...best practises when designing Gantt charts!":3},
    lookAtT="There's a teacher with a friendly expression on her face writing something on the whiteboard.\n"
            '"Come in, come in!" She beacons you over.', #todo: make different for every wrongroom
    longT=f"The exit is to your south.\n"
            "There's a teacher getting ready for class.\n"
            "A student is franticly working on their laptop.\n"
            "> You can [wait] to wait until the lessons start, if you want.", #todo: make different for every wrongroom
)

room201=wrongRoom(  # body language
    name="room201",
    coor=(-1,2,2),
    synonyms=["201"],
    subject1={"    ...how to show confidence in a stressful situation!":3},
    subject2={"    ...the imporance of maintaining eye contact!":3},
    lookAtT="There's a teacher with a confident expression on her face writing something on the whiteboard.\n"
            '"Come in, come in!" She beacons you over.', #todo: make different for every wrongroom
    longT=f"The exit is to your south.\n"
            "There's a teacher getting ready for class.\n"
            "A student is franticly working on their laptop.\n"
            "> You can [wait] to wait until the lessons start, if you want.", #todo: make different for every wrongroom
)

room203=wrongRoom(  # social media consultant
    name="room203",
    coor=(-3,2,2),
    synonyms=["203"],
    subject1={"    ...how to set quantitative targets for your SME's social media campaign!":3},
    subject2={"    ...how to tailor your advertising campaign to small children!":3},
    lookAtT="There's a teacher with a determined expression on her face writing something on the whiteboard.\n"
            '"Come in, come in!" She beacons you over.', #todo: make different for every wrongroom
    longT=f"The exit is to your south.\n"
            "There's a teacher getting ready for class.\n"
            "A student is franticly working on their laptop.\n"
            "> You can [wait] to wait until the lessons start, if you want.", #todo: make different for every wrongroom
)

room303=wrongRoom(  # vitality coach
    name="room303",
    coor=(-3,2,3),
    synonyms=["303"],
    subject1={"    ...how to find the work-life balance that works for you!":3},
    subject2={"    ...three easy mindfullness exercises for on the loo!": 3},
    lookAtT="There's a teacher with an energetic expression on her face writing something on the whiteboard.\n"
            '"Come in, come in!" She beacons you over.', #todo: make different for every wrongroom
    longT=f"The exit is to your south.\n"
            "There's a teacher getting ready for class.\n"
            "A student is franticly working on their laptop.\n"
            "> You can [wait] to wait until the lessons start, if you want.", #todo: make different for every wrongroom
)

room305=wrongRoom(  # dog massage for beginners
    name="room305",
    coor=(1,-1,3),
    synonyms=["305"],
    subject1={"    ...how to promote your pet's overall wellbeing!":3},
    subject2={"    ...how to reduce your pet's stress levels during a thunderstorm!":3},
    lookAtT="There's a teacher with a crazed expression on her face writing something on the whiteboard.\n"
            '"Come in, come in!" She beacons you over.', #todo: make different for every wrongroom
    longT=f"The exit is to your west.\n"
            "There's a teacher getting ready for class.\n"
            "A student is franticly working on their laptop.\n"
            "> You can [wait] to wait until the lessons start, if you want.", #todo: make different for every wrongroom
)

exit = Room(
    name="exit",
    coor=(0,-1,0),
    shortT="You exit the building.",
    longT="You breathe in the fresh air.\n"
          "To your north is the Syntra building.\n"
          "You contemplate if you should [go home]'.",
    lookL=[],
    lookAtT="You look at the automatic doors. You came in this way.",
    exitsL=["n", "go home"],
    synonyms=[]
)

bar = Room(
    name="bar",
    coor=(-1,0,0),
    shortT="You are in a mostly empty bar.",
    longT="This is quite a spatious area. Its size accentuates its emptiness.\n"
          "A staff member is washing up behind the counter.\n"
          "To your east is the lobby.",
    lookL=["barista"],
    askL=["barista"],
    exitsL=["e"],
    takeD={"coffee": "There's a massive espresso machine in the back.",
           "beer": "A variety of beers are on display."},
    lookAtT= "You pick up the faint smell of freshly ground coffee. The bar is open.",
    synonyms=["cafe","café","pub"]

)