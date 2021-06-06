import random
from enum import Enum
import mysql.connector

playableClasses = ['Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
playableBackgrounds = []
playableRaces = []
skills = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
savingThrows = skills
N = 6
Skills = Enum('Skills', 'STRENGTH, DEXTERITY, CONSTITUTION, INTELLIGENCE, WISDOM, CHARISMA')

Classes = Enum('DndClasses', 'ARTIFICER, BARBARIAN, BARD, CLERIC, DRUID, FIGHTER, MONK, PALADIN, RANGER, ROGUE, SORCERER, WARLOCK, WIZARD')
class DndClass():
    def __init__(self, name):
        self.name = name
    
    def levelUp(self):
        print("Todo: add level up for classes")


class Character():
    def __init__(self, race, dndClass, background, level):
        self.race = race
        self.dndClass = dndClass
        self.background = background
        self.stats = self.placeStats()
        self.level = level
        for _ in range(level - 1):
            self.levelUp()

    def placeStats(self):
        statArray = generateStatArray()
        #priorityArray = generatePriorityArray(self.class)
        priorityArray = [6, 0, 2, 3, 1, 5] #todo: generatePriorityArray function
        stats = [0]*N

        for _ in range(N):
            currPrio = min(priorityArray)
            indexPrio = priorityArray.index(currPrio)
            priorityArray[indexPrio] = N + 1 #removing from array would cause indexing issues. This sets the priority above the number of skills, so it will not be reached

            currStat = max(statArray)
            indexStat = statArray.index(currStat)
            statArray[indexStat] = 0 #removing from array would cause indexing issues. This sets the stat to 0, so it will not be reached

            stats[indexPrio] = currStat

        print(stats)

        if (self.race['stat1id'] != None):
            stats[self.race['stat1id'] - 1] += self.race['bonus1']
        
        if (self.race['stat2id'] != None):
            stats[self.race['stat2id'] - 1] += self.race['bonus2']

        if (self.race['stat3id'] != None):
            stats[self.race['stat3id'] - 1] += self.race['bonus3']
        print(stats)
        return stats
    
    def levelUp(self):
        self.dndClass.levelUp()
            

def rollStat():
    stats = []
    for i in range(4):
        stats.append(random.randint(1, 6))
    stats.remove(min(stats))
    return sum(stats)


def generateStatArray(): 
    stats = []
    for i in range(6):
        stats.append(rollStat())
    return stats

def generatePriorityArray():
    priority = []
    for i in range(6):
        priority.append(i)
    return priority

def fetchRaces():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jDAN0921",
        auth_plugin='mysql_native_password',
        database='npc_mancer_db'
    )

    mycursor = db.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM RACES")
    for race in mycursor:
        playableRaces.append(race);

def getRace(name):
    return list(filter(lambda race : race['name'] == name, playableRaces))[0]


fetchRaces()
steve = Character(getRace("High Elf"), 'ranger', 'urchin', 1)

