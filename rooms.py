import sys
from entities_objectives import *

coor = [0,0,0]  # coordinates x,y,z
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
    def __init__(self,name,coor,shortT,longT,lookL,exitsL,useL=[],askL=[],takeD={}):
        self.name = name
        self.coor = coor
        self.shortT = shortT
        self.longT = longT
        self.lookL = lookL
        self.useL = useL
        self.askL = askL
        self.takeD = takeD
        self.exitsL = exitsL
        roomCoorD[self.coor] = self.name

    def checkIfPresent(self,ele,rList):
        return True if ele in rList else False

    def look(self):
        print(self.longT)
        if self.takeD:
            [print(values) for values in self.takeD.values()] #if there are valid items, will print description

    def enter(self): #enters the new room, prints the new room's name and looks around
        currentRoom = roomFromCoor(coor)
        print(currentRoom.shortT)
        print(currentRoom.longT)
        return currentRoom




class Stairs(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def climbStairsExhaustion(self): #If you climb to many stairs, you will become tired
        player.nStairsClimbed+=1
        if player.nStairsClimbed > 2:
            manyStairsClimbed.complete(player.nStairsClimbed)


class Hallway(Room):
    def __init__(self,name,coor,exitsL,takeD={},
                 classroomLocked=True,
                 lookL=[],useL=["key"], shortT = "You are in a hallway.", longT=""):
        self.name = name
        self.coor = coor
        self.classroomNumber = self.name[-3:]
        self.classroomLocked = classroomLocked
        self.useL = useL
        self.lookL = lookL
        self.shortT = shortT
        self.longT = longT
        self.exitsL = exitsL
        roomCoorD[self.coor] = self.name
        self.takeD = takeD

        if self.name.endswith("1"):
            self.longT=f"To your north is classroom {self.classroomNumber}.\n" \
                       f"To your east is the stairwell.\n" \
                       f"The hallway continues to your west."
        elif self.name.endswith("2"):
            self.longT=f"To your north is classroom {self.classroomNumber}.\n" \
                  f"The hallway continues to your east and to your west."
        elif self.name.endswith("3"):
            self.longT=f"To your north is classroom {self.classroomNumber}.\n" \
                  f"This is the end of the hallway. You can go back east."
        elif self.name.endswith("4"):
            self.longT=f"To your west is classroom {self.classroomNumber}.\n" \
                  f"To your north is the stairwell.\n" \
                  f"The hallway continues to your south."
        elif self.name.endswith("5"):
            self.longT=f"To your west is classroom {self.classroomNumber}.\n" \
                  f"The hallway continues to your north and to your south."
        elif self.name.endswith("6"):
            self.longT=f"To your west is classroom {self.classroomNumber}.\n" \
                  f"This is the end of the hallway. You can go back north."


#FIRST FLOOR HALLWAYS
hallway101 = Hallway(
    name="hallway101",
    coor=(-1,1,1),
    exitsL=["e","w","n"]
)

hallway102 = Hallway(
    name="hallway102",
    coor=(-2,1,1),
    exitsL=["e","w","n"]
)

hallway103 = Hallway(
    name="hallway103",
    coor=(-3,1,1),
    exitsL=["e","n"]
)

hallway104 = Hallway(
    name="hallway104",
    coor=(0,0,1),
    exitsL=["e","s","n"]
)

hallway105 = Hallway(
    name="hallway105",
    coor=(0,-1,1),
    exitsL=["e","s","n"]
)

hallway106 = Hallway(
    name="hallway106",
    coor=(0,-2,1),
    exitsL=["e","n"]
)

#SECOND FLOOR HALLWAYS
hallway201 = Hallway(
    name="hallway201",
    coor=(-1,1,2),
    exitsL=["e","w","n"]
)

hallway202 = Hallway(
    name="hallway202",
    coor=(-2,1,2),
    exitsL=["e","w","n"]
)

hallway203 = Hallway(
    name="hallway203",
    coor=(-3,1,2),
    exitsL=["e","n"]
)

hallway204 = Hallway(
    name="hallway204",
    coor=(0,0,2),
    exitsL=["e","s","n"]
)

hallway205 = Hallway(
    name="hallway205",
    coor=(0,-1,2),
    exitsL=["e","s","n"]
)

hallway206 = Hallway(
    name="hallway206",
    coor=(0,-2,2),
    exitsL=["e","n"]
)



#THIRD FLOOR HALLWAYS
hallway301 = Hallway(
    name="hallway301",
    coor=(-1,1,3),
    exitsL=["e","w","n"]
)

hallway302 = Hallway(
    name="hallway302",
    coor=(-2,1,3),
    exitsL=["e","w","n"]
)

hallway303 = Hallway(
    name="hallway303",
    coor=(-3,1,3),
    exitsL=["e","n"]
)

hallway304 = Hallway(
    name="hallway304",
    coor=(0,0,3),
    exitsL=["e","s","n"]
)

hallway305 = Hallway(
    name="hallway305",
    coor=(0,-1,3),
    exitsL=["e","s","n"]
)

hallway306 = Hallway(
    name="hallway306",
    coor=(0,-2,3),
    exitsL=["e","n"]
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
    lookL = ["receptionist","bar","exit","display"],
    askL = ["receptionist"],
    takeD = {"pen":"A Syntra-branded pen is laying on the reception desk."},
    exitsL = ["n","s","w"]
)

toilets = Room(
    name="toilets",
    coor=(1,1,1),
    shortT= "You enter the lavatory.",
    longT="You can [use] the toilets here."
          "To your west is the stairwell. It's the only exit.",
    lookL=["toilet"],
    exitsL = ["w"],
    useL=["toilet"]
)



stairs0 = Stairs(
    name="stairs0",
    coor=(0,1,0),
    shortT = "You are in the stairwell on the ground floor.",
    longT = "To your south is the Lobby.\n"
            "The classrooms are upstairs.",
    lookL = [],
    exitsL = ["s","u"]
)

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
    exitsL = ["s","e","w","u","d"]
)

#pythonClassroom = Room(
 #   name="pythonClassroom",
  #  coor=
#)

#otherClassroom = Room(
 #   name = "otherClassroom",
#)

stairs2 = Stairs(
    name="stairs2",
    coor=(0,1,2),
    shortT = "You are near the stairs on the second floor.",
    longT = "Classrooms 201-203 are to your west.\n"
            "Classrooms 204-206 are to your south.\n"
            "There are more classrooms upstairs.\n"
            "You can take the steps back down to the first floor.",
    lookL = [],
    exitsL = ["s","w","u","d"]
)

stairs3=Stairs(
    name = "stairs3",
    coor=(0,1,3),
    shortT = "You are near the stairs on the third floor.",
    longT = "This is the top floor.\n"
            "Classrooms 301-303 are to your west.\n"
            "Classrooms 304-306 are to your south.\n"
            "You can take the steps back down to the second floor.",
    lookL = [],
    exitsL = ["s","w","d"]
)

outside = Room(
    name="outside",
    coor=(0,-1,0),
    shortT="You exit the building.",
    longT="You breathe in the fresh air.\n"
          "To your north is the Syntra building.\n"
          "You contemplate if you should [go home]'.",
    lookL=[],
    exitsL=["n", "go home"]
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
           "beer": "A variety of beers are on display."}
)