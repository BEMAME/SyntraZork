print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *
import datetime
import random
import time


class GameC:
    def __init__(self, timeNow, laterThan2230,laterThan2200,laterThan1900,laterThan2035,laterThan2020,
                 recess=True,timeVerbose=False, coor=[0,0,0], gameStart=True):
        self.laterThan2230 = laterThan2230
        self.laterThan2200 = laterThan2200
        self.laterThan2035 = laterThan2035
        self.laterThan2020 = laterThan2020
        self.laterThan1900 = laterThan1900
        self.recess = recess
        self.coor = coor
        self.timeNow = timeNow
        self.timeVerbose = timeVerbose
        self.gameStart = gameStart

    def synonymCheck(self, inputVal):
        try:
            x = [target for target, syn in synonymsD.items() if inputVal in syn][0]
            return x  # this returns the key of the synonymsD dictionary
        except:
            None

    def passTime(self,howLong):
        if howLong == "vShort":  # a second or two
            x = list(range(1,3))
            x = random.choice(x)
            print("> A second passes...") if self.timeVerbose is True else None

        elif howLong == "short":  # about 10-20 seconds
            x = list(range(10,24))
            x = random.choice(x)
            print("> A few seconds pass...") if self.timeVerbose is True else None

        elif howLong == "medium":  # about 30-40 seconds
            x = list(range(46,70))
            x = random.choice(x)
            print("> A minute passes...") if self.timeVerbose is True else None

        elif howLong == "long":  # about 4 minutes
            x = list(range(220,250))
            x = random.choice(x)
            print("> A few minutes pass...") if self.timeVerbose is True else None

        elif howLong == "vLong":  # about 30 minutes
            x = list(range(1700,1900))
            x = random.choice(x)
            print("> A half hour passes...") if self.timeVerbose is True else None

        else:
            x = howLong

        game.timeNow = game.timeNow + datetime.timedelta(seconds=x)

    def displayTime(self):
        print(f"You look at your phone. It's {game.timeNow.time()}.")

    def helpMenu(self):
        print("[n] to go North\n"
              "[e] to go East\n"
              "[s] to go South\n"
              "[w] to go West\n"
              "[u] to go Up\n"
              "[d] to go Down\n"
              "[look] to look around the room\n"
              "[talk <person>] to start a conversation\n"
              "[hello <person>] to greet someone\n"
              "[look <object>] to look at an object\n"
              "[use <object>] to use and object\n"
              "[take <object>] to pick up an object\n"
              "[i] to show a list of items that you have with you\n"
              "[score] to display your current score\n"
              "[time] to look at the time\n"
              "[timeVerbose] to toggle updates on time passing off or on (default is off)\n"
              "[wait <number>] to wait a number of minutes you specify\n"
              "[q] to quit (or better: walk outside of the building)")

    def walkInp(self):  # Returns new room if valid direction input,
                        # returns true/false is for checking if valid input given
        if len(inp.split()) > 1 and inp.lower() != "go home":
            return False, player.currentRoom

        if inp.lower() not in ["n", "e", "s", "w", "u", "d", "go home"]:
            return False, player.currentRoom

        if player.currentRoom.checkIfPresent(inp,player.currentRoom.exitsL):
            tryCoor = self.coor.copy()
            if inp.lower() == "n":
                tryCoor[1] = tryCoor[1]+1
            elif inp.lower() == "e":
                tryCoor[0] = tryCoor[0]+1
            elif inp.lower() == "s":
                tryCoor[1] = tryCoor[1]-1
            elif inp.lower() == "w":
                tryCoor[0] = tryCoor[0]-1
            elif inp.lower() == "u":
                tryCoor[2] = tryCoor[2]+1
                player.currentRoom.climbStairsExhaustion()
            elif inp.lower() == "d":
                tryCoor[2] = tryCoor[2]-1
            elif inp.lower() == "go home":  # this can only be selected from the "Exit" room
                game.endGame()

            if roomFromCoor(tryCoor).tryEnter() is True:
                self.coor = tryCoor.copy()
                player.currentRoom = roomFromCoor(self.coor)
                game.passTime("short")
                if player.notInClassOnTime is True and player.currentRoom.name in allRoomL:
                    notInClassroomOnTime.complete()

                return True, player.currentRoom.enter()

            else:
                return True, player.currentRoom
        else:
            print(f"You cannot go that way.")
            return True,player.currentRoom

    def checkInputLen(self):  # is called when player enters 3 words or more - this is not allowed
        if len(inp.split()) > 2:
            print("You entered too many words. To interact with something or someone type '<action> <object',\n"
                  "e.g. 'ask receptionist' or 'look laptop'.")
            return True

        else:
            return False

    def optionsInp(self):  # various meta-options. Return true/false is for checking if valid input given
        if inp.split()[0].lower() not in ["help", "coor", "where", "location", "score", "points", "i", "inv",
                                          "inventory", "backpack","drink","eat","share","time","timeverbose","wait",
                                          "cry", "return"]:
            return False

        if inp.lower() == "help":
            game.helpMenu()
            return True

        if inp.lower() == "time":
            game.displayTime()
            game.passTime("vShort")
            return True

        if inp.lower() == "cry":
            game.passTime("short")
            print("You let it all go.")
            emotions.complete()
            return True

        if inp.lower() == "return key" and player.currentRoom.name=="lobby" and "key" in player.inv:
            game.passTime("short")
            print("You return the breakroom key to the reception.")
            player.inv.remove("key")
            player.changeScore(1)

        if inp.split()[0].lower() == "wait":
            if len(inp.split()) == 1:
                print("How many minutes do you want to wait?")
                return True

            try:  # check if integer
                int(inp.split()[1])
            except:
                print('How long do you want to wait? Type "wait" followed by the number of minutes you want to wait.')
                return True

            x=datetime.timedelta(minutes=int(inp.split()[1]))

            if x < datetime.timedelta(seconds=0):
                timetravel.complete()
                return True
            elif x > datetime.timedelta(minutes=10):
                print("You can only wait up to 10 min at a time. Wouldn't want you to get bored!")
                return True
            else:
                y = input(f"> Are you sure you want to wait {round(x.seconds/60)} minutes?\n"
                      "> Type [y] to confirm, or press enter to cancel. ___"
                      )

                if y != "y":
                    return True

                print(f"> You patiently wait {int(inp.split()[1])} minutes.")
                game.passTime(x.seconds+1)

            return True

        if inp.lower() == "timeverbose":
            if game.timeVerbose is False:
                game.timeVerbose = True
                print("> [SYSTEM] Messages on time passing ENABLED.")
            else:
                game.timeVerbose = False
                print("> [SYSTEM] Messages on time passing DISABLED.")
            return True

        if inp.split()[0].lower() in ["drink","eat"]:
            print('Try "use" to consume food or drinks.')
            return True

        elif inp.lower() == "share coffee" and "coffee" in player.inv and player.currentRoom.name=="room105":
            shareCoffee.complete()
            game.passTime("medium")
            return True

        elif inp.lower() in ["coor", "where", "location"]:
            print(f"{player.currentRoom.shortT} Your coordinates are {game.coor}.")
            return True

        elif inp.lower() in ["score", "points"]:
            player.prtScore()
            return True

        elif inp.lower() in ["i", "inv", "inventory", "backpack"]:
            player.inventory()
            return True

    # looking around the room. Return true/false is for checking if valid input given
    def lookInp(self):
        if inp.split()[0].lower() not in ["look"]:
            return False

        # player typed "look" or "look room" ==> give description of room
        if len(inp.split()) == 1 or inp.lower() == "look room":
            player.currentRoom.look()
            game.passTime("vShort")
            return True

        # player typed "look <something>"
        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())

            #special
            if inp.split()[1].lower() == "inside" and type(player.currentRoom).__name__ == "Hallway":
                x = f"room{player.currentRoom.name[-3:]}"
                str_to_class(x).lookAt()
                game.passTime("short")
            elif x in player.currentRoom.lookL and x in roomCoorD.values():  # looking at an adjacent room
                str_to_class(x).lookAt()
                game.passTime("short")
            elif x in player.inv:
                str_to_class(x).look()
                game.passTime("vShort")
            elif x in player.currentRoom.lookL:  # entities that cannot be taken (e.g. lobby display)
                str_to_class(x).look()
                game.passTime("short")
            elif x in player.currentRoom.takeD:  # things that are laying in the room but haven't been picked up
                print(player.currentRoom.takeD[x])
                game.passTime("vShort")
            else:
                print("I don't understand what you want to look at.")

        return True

    def askInp(self):
        if inp.split()[0].lower() not in ["talk","ask","call"]:
            return False

        if len(inp.split()) == 1:
            print("Who are you talking to?")

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())

            if x == "teacher" and poignantQuestion.done is False and game.recess is True and game.laterThan1900 is True:
                poignantQuestion.complete()
                return True

            if x in player.currentRoom.askL:
                if str_to_class(x).ask() is True:
                    game.passTime(str_to_class(x).askTime)
            elif x in player.inv:
                print(f"{x.capitalize()} isn't feeling very talkative.")
            else:
                print(f"No {x} in sight. Is this what lonelyness feels like?")

        return True

    def helloInp(self):
        if inp.split()[0].lower() not in ["hello", "greet", "hi"]:
            return False

        if len(inp.split()) == 1:
            print("Who are you talking to?")

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            if x in player.currentRoom.askL:
                str_to_class(x).hello()
                game.passTime("short")
            elif x in player.inv:
                print(f"{x.capitalize()} isn't feeling very talkative.")
            else:
                print(f"No {x} in sight. Is this what loneliness feels like?")
        return True

    def takeInp(self):
        if inp.split()[0].lower() not in ["get","grab","take"]:
            return False

        if len(inp.split()) == 1:
            print(f"What do you want to {inp.split()[0].lower()}?")
            return True

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            if isinstance(x,str) is False:
                print("I don't understand what you want to take.")

            elif x in player.inv:
                print(f"You already have the {inp.split()[1].lower()}!")

            elif x in player.currentRoom.takeD.keys():  # triggers if the item is in the dict of valid items for taking.
                str_to_class(x).take()
                game.passTime("short")
                return True

            elif isinstance(str_to_class(x),Entity) is True:
                if str_to_class(x).tooHeavy is True:
                    print(f"You can't pick the {inp.split()[1].lower()} up! You're just a geek,"
                          f" not some sort of strongman jock!")
                    hurtEgo.complete()
                else:
                    print(f"I'm not sure how you would grab the {inp.split()[1].lower()} from here...")

            # an easter egg objective
            elif inp.split()[1].lower() == "points":
                getPoints.complete()

        return True

    def useInp(self):

        if inp.split()[0].lower() not in ["use"]:
            return False

        if len(inp.split()) == 1:
            print(f"What do you want to {inp.split()[0].lower()}?")
            return True

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            n = 'an' if inp.split()[1].lower()[0] in ["a","e","i","o","u"] else 'a'  # "a pen" versus "an objective"

            if x == "laptop" and player.currentRoom.name == "room102" and installPyCharm.done is False:
                game.passTime("long")
                if game.timeNow > datetime.datetime(2022, 9, 20, 19, 00, 00):
                    installPyCharmTooLate.complete()
                    installPyCharm.done = True
                    installPyCharm.active = False
                else:
                    installPyCharm.complete()

            elif x in player.inv or x in player.currentRoom.useL:
                if str_to_class(x).use() is True:  # successfully used something
                    game.passTime(str_to_class(x).useTime)  # how long it takes depends on what you use, default = "short"

            elif x in synonymsD:
                print(f"You don't have {n} {inp.split()[1].lower()}.")

            else:
                print(f"What's {n} {inp.split()[1].lower()}?")
            return True

    def learnInp(self):
        if inp.lower() != "learn":
            return False

        if player.currentRoom.name in allRoomL:
            if game.recess is True:
                print("There are no classes being taught right now.")
            elif self.laterThan2035 is True:
                if player.currentRoom.name == "room101":
                    learnPM2.complete()
                if player.currentRoom.name == "room102":
                    learnPython2.complete()
                if player.currentRoom.name == "room203":
                    learnSMC2.complete()
                if player.currentRoom.name == "room201":
                    learnBodyLang2.complete()
                if player.currentRoom.name == "room303":
                    learnBodyVitaCoach2.complete()
                if player.currentRoom.name == "room305":
                    learnDogMassa2.complete()
                player.thingsLearned.update(player.currentRoom.subject2)
                game.timeNow = datetime.datetime(2022, 9, 20, 22, 1, 3)
            elif self.laterThan1900 is True:
                if player.currentRoom.name == "room101":
                    learnPM1.complete()
                if player.currentRoom.name == "room102":
                    learnPython1.complete()
                if player.currentRoom.name == "room203":
                    learnSMC1.complete()
                if player.currentRoom.name == "room201":
                    learnBodyLang1.complete()
                if player.currentRoom.name == "room303":
                    learnBodyVitaCoach1.complete()
                if player.currentRoom.name == "room305":
                    learnDogMassa1.complete()
                player.thingsLearned.update(player.currentRoom.subject1)
                game.timeNow = datetime.datetime(2022, 9, 20, 20, 20, 58)
        return True

    def invalidAction(self):
        print("I don't understand what you want to do. Type [help] for a list of basic commands.")

    def endGame(self):
        if player.score < 0:  # horrible ending
            print(f"You cannot bear this any longer. You run towards your bicycle and ride off as fast as you can.\n"
                  f"When you look behind you, you see the Syntra building disappear behind the horizon.\n"
                  f"You swear never to return again.")
        elif -1 < player.score < 10:  # bad ending
            print(f"You sigh as walk towards your bicycle. Learning about Python was tougher than you thought.\n"
                  "On the way home, you contemplate quitting your Syntra course.")
        elif player.score > 9:  # good ending
            print(f"Satisfied, you walk towards your bicycle.\n"
                  "On the way home, many ideas for your future project come to mind.\n"
                  "You jot them down on a piece of paper as soon as you get home.")

        input("\n(press Enter to continue)\n")

        if wrongRegisterSigned.done is True:
            print(f"You signed the wrong register!")
            player.changeScore(-1)

            input("\n(press Enter to continue)\n")

        if penStolen.done is True:
            print(f"You put the stolen pen on display on the mantlepiece.\n"
                  f"What a chump that student was!")
            player.changeScore(1)

            input("\n(press Enter to continue)\n")

        if "beer" in player.inv:
            print(f"After a long day you're finally home!\n"
                  f"You sit down on your couch and crack open the heavy beer you got from the bar.")
            player.changeScore(4)

            input("\n(press Enter to continue)\n")

        if len(player.thingsLearned) == 0:
            print(f"You have learned nothing of use this evening. What a waste!")
            player.changeScore(-10)
            input("\n(press Enter to continue)\n")

        else:
            print(f"Today you've learned...")
            for x in player.thingsLearned.keys():
                time.sleep(1)
                print(x)
                time.sleep(1)
            time.sleep(1)
            print("")
            player.changeScore(sum(player.thingsLearned.values()))
            input("\n(press Enter to continue)\n")

        if "key" in player.inv:
            print(f"A few days later you find the key with the massive keychain in your backpack. Whoops!")
            player.changeScore(-1)
            input("\n(press Enter to continue)\n")

        print(f" ~~You finished the game with a score of {player.score}! Thanks for playing!")

        time.sleep(10)
        input("\nPress any button to quit.\n")
        sys.exit()

game = GameC(timeNow=datetime.datetime(2022, 9, 20, 18, 52, 11),
             laterThan2230 = False,
             laterThan2200 = False,
             laterThan2035 = False,
             laterThan2020 = False,
             laterThan1900 = False)

while True:
    # setting up the very first room at the start of the game...
    if game.gameStart is True:
        print("------------------------------------------------------------------------------------------------------")
        player.currentRoom = roomFromCoor(game.coor)
        print("A few weeks ago, you registered for the Syntra 'Python for Beginners' class.\n"
              "Full of excitement you enter the Syntra lobby.\n"
              "You should [look] around to find out where to go.\n"
              "> Classes start at 19:00 - make sure to be on time!")
        game.gameStart = False
    inp = input("------------------------------------------------------------------------------------------------------"
                "\nWhat do you do? ___")
    #

    if inp == "":
        print("Type 'help' for an overview of basic commands.")
        continue

    if inp.lower() in ["q", "quit"]:
        break

    #checks what input was given and performs the action
    validAction = []
    walkValidInp, player.currentRoom = game.walkInp()
    validAction.append(walkValidInp)
    validAction.append(game.checkInputLen())
    validAction.append(game.lookInp())
    validAction.append(game.askInp())
    validAction.append(game.helloInp())
    validAction.append(game.takeInp())
    validAction.append(game.useInp())
    validAction.append(game.optionsInp())
    validAction.append(game.learnInp())
    if True not in validAction:
        game.invalidAction()


    #THINGS THAT CHANGE WHEN TIME PASSES
    if game.timeNow > datetime.datetime(2022, 9, 20, 22, 30, 00) and game.laterThan2230 is False:
        game.laterThan2230=True
        drinkCoffee.done = False

        for x in allRoomL:
            str_to_class(x).useL = []
            str_to_class(x).takeD = {}
            str_to_class(x).longT = f"The exit is to your south." \
                                    f"\nYou are alone in an empty classroom."
            str_to_class(x).lookAtT = "An empty classroom."
            str_to_class(x).askL = []
            str_to_class(x).lookL = []

    elif game.timeNow > datetime.datetime(2022, 9, 20, 22, 00, 00) and game.laterThan2200 is False:
        game.laterThan2200 = True
        drinkCoffee.done = False

        print("It's past 22:00. Classes have concluded. Time to wrap up and go home...")
        madeIt.complete()

        if player.currentRoom.name in allRoomL:
            print('The teacher wraps up. "See you all next week!"')


        for x in allRoomL:
            str_to_class(x).useL=[]
            str_to_class(x).takeD={}
            str_to_class(x).longT=f"The exit is to your south." \
                                  f"\nClass has finished. The teacher is packing up."
            str_to_class(x).lookAtT="The class has ended."
            str_to_class(x).askL=["teacher"]
            str_to_class(x).lookL=["teacher"]
        teacher.askT="The teacher smiles at you.\n" \
                     '"Enthousiastic about the course material, eh? Have a rest, we can answer your question next week."'
        teacher.lookT="The teacher is packing up."

        receptionist.askT='When the receptionist sees you, she looks up.\n' \
                          '"Oh, excuse me! We\'re still missing one breakroom key..."' \
                          '> You should [return key] to the reception. It\'s useless to you anyway...'

        receptionist.helloT='When the receptionist sees you, she looks up.\n' \
                          '"Oh, excuse me! We\'re still missing one breakroom key..."' \
                          '> You should [return key] to the reception. It\'s useless to you anyway...'

        if penBorrowed.done is True:
            time.sleep(1)
            print("The student approaches you.\n"
                  '"Hey, I think you still have my pen, am I right?"')
            while x.lower not in ["y","yes","n","no"]:
                x = input("> Do you answer [yes] or [no]? ___")
                if x.lower() in ["y", "yes"]:
                    player.inv.remove("pen")
                    penReturned.complete()
                    penBorrowed.done = False
                    break
                else:
                    penStolen.complete()
                    penBorrowed.done = False
                    break
            print("------------------------------------------------------------------------------------------------------")

    elif game.timeNow > datetime.datetime(2022, 9, 20, 20, 35, 00) and game.laterThan2035 is False:
        game.laterThan2035 = True
        drinkCoffee.done = False
        game.recess = False

        if player.currentRoom.name in allRoomL:
            print('"Alright everyone, let\'s continue with the lesson at hand!" The teacher addresses the class.')
            inClassroomOnTime.complete()
        else:
            player.notInClassOnTime=True

        for x in allRoomL:
            str_to_class(x).longT = f"The exit is to your south." \
                                    f"\nA teacher is in the middle of an explanation." \
                                    f"\nA student is eagerly paying attention." \
                                    f"\n> Type [learn] to pay attention to class. Time will proceed rapidly."
            str_to_class(x).lookAtT = "The class is in session.\n"
            '"Ah, a latecomer! Come on in!" The teacher beacons you over.'
            str_to_class(x).askL=["teacher","student"]
            str_to_class(x).lookL=["teacher","student"]


        teacher.askT = "You have a question on your mind, but you don't want to interrupt\n" \
                       "the teacher in the middle of their explanation..."
        room105.lookAtT="The lights are on, but nobody's there.\n" \
                        "You spot a large, insulated dispenser on one of the tables, alongside some cups."

        findBreakRoom.active = False

    elif game.timeNow > datetime.datetime(2022, 9, 20, 20, 20, 00) and game.laterThan2020 is False:
        game.laterThan2020 = True
        game.recess = True
        drinkCoffee.done = False
        player.notInClassOnTime = False

        #todo bar closed but beer still there

        if player.currentRoom.name in allRoomL:
            print('The teacher concludes: "... but we\'ll let that sink in for now.'
                  ' Let\'s have a break until 20:35, ok?')

        print("It's break time! Classes are in recess until 20:35.\n"
              "> You could consider a bathroom break or to visit the breakroom.")

        for x in allRoomL:
            str_to_class(x).useL=["register"]
            str_to_class(x).longT=f"The exit is to your south." \
                                  f"\nClass is in recess. Only the teacher is present - they are checking their emails."
            str_to_class(x).lookAtT="The class is in recess. Only the teacher is present"
            str_to_class(x).askL=["teacher"]
            str_to_class(x).lookL=["teacher","key","register"]

        teacher.askT='You ask the teacher where the breakroom is.\n' \
                     '"Good question that. Best to ask the reception desk."'
        findBreakRoom.active=True
        teacher.lookT="The teacher is checking their emails."
        receptionist.askT="You can't thing of anything to ask the receptionist."


    elif game.timeNow > datetime.datetime(2022, 9, 20, 19, 00, 00) and game.laterThan1900 is False:
        game.laterThan1900 = True
        print("It's past 19:00. Classes have started.")
        game.recess = False

        if player.currentRoom.name in allRoomL:
            inClassroomOnTime.complete()
        else:
            player.notInClassOnTime = True

        for x in allRoomL:
            str_to_class(x).longT=f"The exit is to your south." \
                                  f"\nA teacher is in the middle of an explanation." \
                                  f"\nA student is eagerly paying attention." \
                                  f"\n> Type [learn] to pay attention to class. Time will proceed rapidly."
            str_to_class(x).lookAtT="The class is in session.\n"
            '"Ah, a latecomer! Come on in!" The teacher beacons you over.'
        teacher.askT="You have a question on your mind, but you don't want to interrupt\n" \
                     " the teacher in the middle of their explanation..."
