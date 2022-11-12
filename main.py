print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *
import datetime
import random
import time


class GameC:
    def __init__(self, timeNow, laterThan2230,laterThan2200,laterThan2130,laterThan2100,laterThan2030,laterThan2000,
                 timeVerbose=False, coor=[0,0,0], gameStart=True):
        self.laterThan2230 = laterThan2230
        self.laterThan2200 = laterThan2200
        self.laterThan2130 = laterThan2130
        self.laterThan2100 = laterThan2100
        self.laterThan2030 = laterThan2030
        self.laterThan2000 = laterThan2000
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
                                          "inventory", "backpack","drink","eat","share","time","timeverbose","wait"]:
            return False

        if inp.lower() == "help":
            game.helpMenu()
            return True

        if inp.lower() == "time":
            game.displayTime()
            game.passTime("vShort")
            return True

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
            elif x >= datetime.timedelta(minutes=30):
                y = input("> Are you sure you want to wait that long?\n"
                          "> Type [y] to confirm, or press enter to cancel. ___")
                if y != "y":
                    return True
            print(f"> You patiently wait {int(inp.split()[1])} minutes.")
            game.passTime(x.seconds+1)
            game.displayTime()

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
            if x in player.currentRoom.askL:
                str_to_class(x).ask()
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
                print(f"No {x} in sight. Is this what lonelyness feels like?")
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

            if x in player.inv or x in player.currentRoom.useL:
                if str_to_class(x).use() is True:  # successfully used something
                    game.passTime(str_to_class(x).useTime)  # how long it takes depends on what you use, default = "short"

            elif x in synonymsD:
                print(f"You don't have {n} {inp.split()[1].lower()}.")

            else:
                print(f"What's {n} {inp.split()[1].lower()}?")

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
                  "On the way home, you contemplate quitting the Python for beginners course.")
        elif player.score > 9:  # good ending
            print(f"Satisfied, you walk towards your bicycle.\n"
                  "On the way home, many ideas for your Python project come to mind.\n"
                  "You jot them down on a piece of paper before you go to bed.")

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

game = GameC(timeNow=datetime.datetime(2022, 9, 20, 19, 52, 11),
             laterThan2230 = False,
             laterThan2200 = False,
             laterThan2130 = False,
             laterThan2100 = False,
             laterThan2030 = False,
             laterThan2000 = False)

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
    if True not in validAction:
        game.invalidAction()


    #THINGS THAT CHANGE WHEN TIME PASSES
    if game.timeNow > datetime.datetime(2022, 9, 20, 22, 30, 00) and game.laterThan2230 is False:
        game.laterThan2230=True
        drinkCoffee.done = False
        
    elif game.timeNow > datetime.datetime(2022, 9, 20, 22, 00, 00) and game.laterThan2200 is False:
        game.laterThan2200 = True
        drinkCoffee.done = False
    
    elif game.timeNow > datetime.datetime(2022, 9, 20, 21, 30, 00) and game.laterThan2130 is False:
        game.laterThan2130 = True
        drinkCoffee.done = False

    elif game.timeNow > datetime.datetime(2022, 9, 20, 21, 00, 00) and game.laterThan2100 is False:
        game.laterThan2100 = True
        drinkCoffee.done = False
        
    elif game.timeNow > datetime.datetime(2022, 9, 20, 20, 30, 00) and game.laterThan2030 is False:
        game.laterThan2030 = True
        drinkCoffee.done = False

    elif game.timeNow > datetime.datetime(2022, 9, 20, 20, 00, 00) and game.laterThan2000 is False:
        game.laterThan2000 = True

