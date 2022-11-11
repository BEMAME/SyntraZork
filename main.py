print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
      "\n~~~~  Welcome to SyntraZork! Input 'help' for options  ~~~~\n"
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

from rooms import *

class GameC:
    def __init__(self, coor=[0,0,0], gameStart=True):
        self.coor = coor
        self.gameStart = gameStart

    def synonymCheck(self, inputVal):
        try:
            x = [target for target, syn in synonymsD.items() if inputVal in syn][0]
            return x  # this returns the key of the synonymsD dictionary
        except:
            None

    def helpMenu(self):
        print("[n] to go North\n"
              "[e] to go East\n"
              "[s] to go South\n"
              "[w] to go West\n"
              "[u] to go Up\n"
              "[d] to go Down\n"
              "[look] to look around the room\n"
              "[talk <person>] to start a conversation\n"
              "[look <object>] to look at an object.\n"
              "[use <object>] to use and object.\n"
              "[take <object>] to pick up an object.\n"
              "[i] to show a list of items that are in your backpack.\n"
              "[score] to display your current score\n"
              "Walk outside of the building to quit")

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
                Game.endGame()

            if roomFromCoor(tryCoor).tryEnter() is True:
                self.coor = tryCoor.copy()
                player.currentRoom = roomFromCoor(self.coor)
                return True, player.currentRoom.enter()
            else:
                print(self.coor)
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
                                          "inventory", "backpack"]:
            return False

        if inp.lower() == "help":
            Game.helpMenu()
            return True

        if inp.lower() in ["coor", "where", "location"]:
            print(f"{player.currentRoom.shortT} Your coordinates are {Game.coor}.")
            return True

        if inp.lower() in ["score", "points"]:
            player.prtScore()
            return True

        if inp.lower() in ["i", "inv", "inventory", "backpack"]:
            player.inventory()
            return True

    # looking around the room. Return true/false is for checking if valid input given
    def lookInp(self):
        if inp.split()[0].lower() not in ["look"]:
            return False

        # player typed "look" or "look room" ==> give description of room
        if len(inp.split()) == 1 or inp.lower() == "look room":
            player.currentRoom.look()
            return True

        # player typed "look <something>"
        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())

            #special
            if inp.split()[1].lower() == "inside" and type(player.currentRoom).__name__ == "Hallway":
                x = f"room{player.currentRoom.name[-3:]}"
                str_to_class(x).lookAt()
            elif x in player.currentRoom.lookL and x in roomCoorD.values():
                str_to_class(x).lookAt()
            elif x in player.inv:
                print("You have a look in your backpack.")
                str_to_class(x).look()
            elif x in player.currentRoom.lookL:  # entities that cannot be taken (e.g. lobby display)
                str_to_class(x).look()
            elif x in player.currentRoom.takeD:  # things that are laying in the room but haven't been picked up
                print(player.currentRoom.takeD[x])
            else:
                print("I don't understand what you want to look at.")



        return True

    def talkInp(self):
        if inp.split()[0].lower() not in ["talk","ask","call"]:
            return False

        if len(inp.split()) == 1:
            print("Who are you talking to?")

        elif len(inp.split()) == 2:
            x = self.synonymCheck(inp.split()[1].lower())
            if x in player.currentRoom.askL:
                str_to_class(x).ask()
            elif x in player.inv:
                print(f"{x.capitalize()} isn't feeling very talkative.")
            else:
                return False

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

            if x in player.inv:
                print(f"You already have the {inp.split()[1].lower()}!")

            elif x in player.currentRoom.takeD:  # triggers if the item is in the dict of valid items for taking.
                str_to_class(x).take()
                return True

            elif isinstance(str_to_class(x),Entity) is True:
                if str_to_class(x).tooHeavy is True:
                    print(f"You can't pick the {inp.split()[1].lower()} up! You're just a geek,"
                          f" not some sort of strongman jock!")
                    hurtEgo.complete()
                else:
                    print(f"There are no {inp.split()[1].lower()}s for you to take...")

            # an easter egg objective
            elif inp.split()[1].lower() == "points":
                getPoints.complete()

            else:
                print(f"{str_to_class(x).name.capitalize()}s are not for the taking.")

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
                str_to_class(x).use()

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
            print(f"You sigh as walk towards your bicycle. You don't feel like you've learned much today.\n"
                  "On the way home, you contemplate quitting the Python for beginners course.")
        elif player.score > 9:  # good ending
            print(f"Satisfied, you walk towards your bicycle.\n"
                  "On the way home, many ideas for your Python project come to mind.\n"
                  "You jot them down on a piece of paper before you go to bed.")

        input("\n(press Enter to continue)")

        if "beer" in player.inv:
            print(f"After a long day you're finally home!\n"
                  f"You sit down on your couch and crack open the heavy beer you got from the bar.")
            player.changeScore(3)

            input("\n(press Enter to continue)")

        if "key" in player.inv:
            print(f"A few days later you find the key with the massive keychain in your backpack.\n"
                  f"> Whoops! You forgot to return the key!")
            player.changeScore(-1)

            input("\n(press Enter to continue)")

        print(f"\n ~~You finished the game with a score of {player.score}! Thanks for playing!")

        self.gameOver = True

        sys.exit()

Game = GameC()

while True:
    # setting up the very first room at the start of the game...
    if Game.gameStart is True:
        print("------------------------------------------------------------------------------------------------------")
        player.currentRoom = roomFromCoor(Game.coor)
        print("A few weeks ago, you registered for the Syntra 'Python for Beginners' class.\n"
              "Full of excitement you enter the Syntra lobby. Classes start in 5 minutes.\n"
              "You should [look] around to find out where to go.")
        Game.gameStart = False
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
    walkValidInp, player.currentRoom = Game.walkInp()
    validAction.append(walkValidInp)
    validAction.append(Game.checkInputLen())
    validAction.append(Game.lookInp())
    validAction.append(Game.talkInp())
    validAction.append(Game.takeInp())
    validAction.append(Game.useInp())
    validAction.append(Game.optionsInp())
    if True not in validAction:
        Game.invalidAction()
