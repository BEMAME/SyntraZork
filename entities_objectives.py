synonymsD = {}  # dict with synonyms for all entities, is populated by entity init


class Entity:
    def __init__(self, name, lookT, synonyms, tooHeavy=False,consumeOnUse=False, useRoom=["ANY"], useT=""):
        self.name = name
        self.lookT = lookT
        self.synonyms = synonyms
        self.tooHeavy = tooHeavy
        self.synonyms.append(self.name)
        self.consumeOnUse = consumeOnUse
        self.useRoom = useRoom
        self.useT = useT
        synonymsD[self.name] = self.synonyms  # this puts the synonyms of each entity into the synonymsD dict

    def look(self):
        print(self.lookT)

        #specials
        if self.name == "receptionist" and findClassRoom.done is False:  # receptionist will ask if you need help
            receptionist.hello()
        elif self.name == "display" and findClassRoom.done is False:
            findClassRoom.complete()


    def use(self):
        if player.currentRoom.name in self.useRoom or "ANY" in self.useRoom:
            print(self.useT) if self.useT != "" else None
            if self.consumeOnUse is True:
                player.inv.remove(self.name)
                print(f"> You no longer have the {self.name}.")

            # specials
            if self.name == "coffee":
                drinkCoffee.complete()
                player.drinks += 1
                player.bladderCheck()
            elif self.name == "beer":
                player.drinks += 3
                if player.classComplete is True:
                    drinkBeerAfter.complete()
                else:
                    drinkBeer.complete()
                player.bladderCheck()
            elif self.name == "toilet":
                if player.drinks > 0:
                    bladderRelief.complete()
                    player.drinks = 0
                else:
                    print("You don't need to use the toilet.")
            elif self.name == "key":
                if breakroomOpened.done is False:
                    print("The key fits the lock.")
                    breakroomOpened.complete()
                    from rooms import room105
                    room105.locked = False
                else:
                    print("The door is already unlocked!")
        else:
            print("You can't use that here.")

class Thing(Entity):
    def __init__(self, onlyOne=True, *args, **kwargs):
        self.onlyOne = onlyOne
        super().__init__(*args, **kwargs)

    def take(self):
        if self.onlyOne is True:
            player.currentRoom.takeD.pop(self.name)  # remove the item from room

        if self.name == "pen":
            getPen.complete()

        elif self.name == "beer":
            if getBeer.done is False:
                player.inv.add(self.name)  # put item in inventory
                getBeer.complete()
            elif getBeer.done is True:
                baristaAnnoyed.complete()
            return

        elif self.name == "coffee":
            player.inv.remove("bottle")
            getCoffee.complete()
        else:
            print(f"You put the {self.name} in your backpack.")

        player.inv.add(self.name)  # put item in inventory

class Person(Entity):
    def __init__(self, helloT, askT, tooHeavy=True,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helloT = helloT
        self.askT = askT
        self.tooHeavy = tooHeavy

    def hello(self):
        print(self.helloT)

    def ask(self):
        from rooms import bar
        if bladderFull.done is True:
            print(f"You ask the {self.name} where the toilets are.\n"
                  f'"First floor, east."')
        elif self.name == "receptionist" and findClassRoom.done is False:
            print(self.askT)
            findClassRoom.complete()
            receptionist.askT = "You don't have any more questions for the receptionist."
        elif self.name == "barista" and baristaAnnoyed.done is True:
            baristaAnnoyed.complete()
        elif self.name == "barista" and bar.takeD == {}:
            print(f"You ask the barista if you can get anything else.")
            baristaAnnoyed.complete()
        elif self.name in ["receptionist","teacher"] and findBreakRoom.done is False and findBreakRoom.active is True:
            print(f"You ask the {self.name} where the breakroom is. "
                  '"Oh ofcourse! Room 105."')
            findBreakRoom.complete()
        else:
            print(self.askT)



class Protagonist:
    def __init__(self, currentRoom="lobby", classComplete=False, nStairsClimbed=0,
                 score=0, drinks=0, inv={"laptop","bottle"}):
        self.currentRoom = currentRoom
        self.classComplete = classComplete
        self.nStairsClimbed = nStairsClimbed
        self.score = score
        self.drinks = drinks
        self.inv = inv

    def changeScore(self, points):
        self.score = self.score + points

        if points == 0:
            return None  # this is needed for repeatable Objectives in which the score for repeating the objective is 0.

        s = lambda x: 'point' if (abs(points) == 1) else 'points'
        if points < 0:
            print(f"> Your score decreased by {abs(points)} {s(points)}.")
        else:
            print(f"> Your score increased by {points} {s(points)}.")

    def inventory(self):
        print("Your backpack contains the following items;")
        print("> ", ', '.join(self.inv))

    def prtScore(self):
        print(f"Your score is {self.score}.")

    def bladderCheck(self):
        if player.drinks > 3:
            bladderFull.complete()

        elif player.drinks > 5:
            bladderDisaster.complete()
            player.drinks = 0


player = Protagonist()


class Objective:
    def __init__(self, completeT, score, completeRoom,done=False,
                 repeatable=False, repeatT="", repeatScore=0, confirmT="",
                 active=True):
        self.completeT = completeT
        self.score = score
        self.completeRoom = completeRoom
        self.done = done
        self.repeatable = repeatable
        self.repeatT = repeatT
        self.repeatScore = repeatScore
        self.confirmT = confirmT
        self.active = active

    def complete(self, xtraTxt=""):
        if player.currentRoom.name in self.completeRoom or "ANY" in self.completeRoom:

            if self.done is False:  # player hasn't completed the objective yet
                self.done = True
                printT=self.completeT.replace("xtraTxt",str(xtraTxt))
                print(printT)
                player.changeScore(self.score)
            elif self.done is True and self.repeatable is True:  # player completes a repeatable objective again
                printT=self.repeatT.replace("xtraTxt",str(xtraTxt))
                print(printT)
                player.changeScore(self.repeatScore)
            elif self.done is True and self.repeatable is False:  # player completes a non-repeatable objective
                printT=self.confirmT.replace("xtraTxt",str(xtraTxt))
                print(printT)

        else:
            print("This is not the right place to use this item...")

# an easter egg
getPoints = Objective(
    completeT="> You grab some points.",
    score=2,
    completeRoom=["ANY"],
    repeatable=True,
    repeatT="> Hey! Don't get greedy now!",
    repeatScore=-1
)

findClassRoom = Objective(
    completeT="> You found which classroom you should go to!",
    score=1,
    completeRoom=["ANY"]
)

findBreakRoom = Objective(
    completeT="> You found the breakroom!",
    score=1,
    completeRoom=["ANY"],
    active=False  # only activates during break
)

hurtEgo = Objective(
    completeT="> Your ego is hurt. Should have known better.",
    score=-1,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT="> Your ego still hurts from the last time..."
)

getPen = Objective(
    completeT='"You can keep that if you want", says the receptionist.\n'
              '> You have a pen!',
    score=1,
    completeRoom=["ANY"]
)

breakroomOpened = Objective(
    completeT="> You've unlocked the breakroom!",
    score=2,
    completeRoom=["hallway105"],
    repeatable=False
)

getBeer = Objective(
    completeT="Without a word, the barkeep gives you one of the heavy beers on display.\n"
              "> You have a beer! Remember to drink responsibly.",
    score=1,
    completeRoom=["ANY"]
)

getCoffee = Objective(
    completeT="The barkeep fills up your Thermos bottle with fresh, hot coffee.\n"
              '> Your bottle was upgraded into coffee!',
    score=1,
    completeRoom=["ANY"]
)

drinkCoffee = Objective(
    completeT="The coffee peps you up.",
    score=1,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT="You've already hit diminishing returns on the coffee.\n"
             "Still tasty, but you no longer feel the caffeine hit."
)

drinkBeer = Objective(
    completeT="The beer reduces your ability to focus on the lessons.\n"
              "> You chose a really bad time to consume alcohol...",
    score=-3,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT=""
)

drinkBeerAfter = Objective(
    completeT="In celebration of finishing the classes, you crack open the beer.\n"
              "After you finish your drink, you feel slightly embarrassed for impulsively\n"
              " consuming alcohol within the Syntra building."
              "> You chose a somewhat unfortunate time for consuming alcohol...",
    score=-3,
    completeRoom=["ANY"],
    repeatable=False,
    confirmT=""
)

manyStairsClimbed = Objective(
    completeT="You getting tired from walking up all these the stairs...",
    score=-1,
    completeRoom=["ANY"],
    repeatable=True,
    repeatT="You've already climbed xtraTxt stairs today...  Your programmer's muscles ache.",
    repeatScore=-1
)

bladderFull = Objective(
    completeT="> All these drinks have filled up your bladder...",
    score=0,
    completeRoom=["ANY"],
    repeatable=True,
    repeatScore=-1,
    repeatT="Although your bladder is already completely full, you decide to fill it up further.\n"
            "> This may end in disaster..."
)

bladderDisaster = Objective(
    completeT="You're too late. Emotions of warmth, relief and embarrassment wash over you.\n"
              "> You've had a little accident.",
    score=-10,
    completeRoom=["ANY"],
    repeatable=True,
    repeatScore=-5,
    repeatT="Once more you piss yourself. This time you're not quite as embarrassed.\n"
            "> You've had another little accident."
)

bladderRelief = Objective(
    completeT="You feel relieved.",
    score=1,
    completeRoom=["Toilets"],
    repeatable=True,
    repeatScore=0,
    repeatT="You have another quick tinkle. Better safe than sorry!"
)

baristaAnnoyed = Objective(
    completeT=f"\"Look, I'm closing up here. Don't you have a class to attend to?\"\n"
                  "> The barkeep wants to close shop.",
    score=0,
    repeatable=True,
    repeatT="The barista slaps his cleaning rag on the counter. \n"
            "\"Please leave. Now.\"\n"
            "> You are intimidated.",
    repeatScore=-1,
    completeRoom=["bar"]
)

receptionist = Person(
    name="receptionist",
    lookT="The receptionist is working on her computer. She is very focused.",
    helloT="With a start, the receptionist looks up at you. 'Oh, good evening. Anything you wanted to [ask]?'",
    synonyms=["reception", "desk"],
    askT="You ask the receptionist which classroom you should be in for the Python for Beginners Class.\n"
         '"Ah, yes. Room 102, first floor. Enjoy!"'
)

barista = Person(
    name="barista",
    lookT="The barkeep is washing up. He does not look up at you.",
    helloT='The barkeep shakes off his hands. "Sup?"',
    synonyms=["barkeep","bartender","barkeeper","server","barman","staff"],
    askT='You ask what you can [get] here. "Beer, coffee?\n"'
         '> The barkeep seems somewhat impatient...'
)

key = Thing(name="key",
            lookT="An unremarkable key with a large keychain.",
            synonyms=[],
            useRoom="hallway105")

pen = Thing(name="pen",
            lookT="The Syntra-branded pen you got from the reception desk.",
            synonyms=[],
            consumeOnUse=False)

laptop = Thing(name="laptop",
               lookT="You look at your tiny laptop. It can barely run PyCharm.",
               synonyms = ["computer"],
               #useRoom= classroom,
               consumeOnUse=False)

bottle = Thing(name="bottle",
               lookT="Your faithful old Thermos bottle. It's mostly empty, just a splash of cold coffee remains.",
               synonyms=["thermos","cup"],
               useT="No matter how hard you slurp, you can't seem to get the last few drops of cold coffee out.",
               consumeOnUse=False)

display = Thing(name="display",
                lookT="The display lists all classes that are given this evening.\n"
                      "~~Social media consultant: Room 203~~\n"
                      "~~Project Management: Room 101~~\n"
                      "~~Python for Beginners: Room 102~~\n"
                      "~~Body Language: Room 201~~\n"
                      "~~Vitality Coach: Room 303~~\n"
                      "~~Dog Massage for Beginners: Room 305~~",
                tooHeavy=True,
                synonyms=[],
                consumeOnUse=False)

coffee = Thing(name="coffee",
               lookT="Your faithful old Thermos bottle, filled with hot coffee from the bar.",
               useT="You take a sip of from your Thermos bottle.",
               synonyms=[],
               consumeOnUse=False)

beer = Thing(name="beer",
             lookT="A specialty beer. Is this the right time to open it?",
             useT="You drink the beer.",
             onlyOne=False,
             synonyms=[],
             consumeOnUse=True)

toilet = Entity(name="toilet",
               tooHeavy=True,
               lookT="Sparkling clean! Very inviting.",
               synonyms=["lavatory","wc"],
               useT=""
               )
