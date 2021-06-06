import random
from enum import Enum
import mysql.connector

playableClasses = ['Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
playableBackgrounds = []
playableRaces = []
selectableSubraces = []
abilities = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
savingThrows = abilities

numProf = 18
numStat = 6

class Character():
    def __init__(self, race, dndClass, background, level):
        self.race = race
        self.dndClass = dndClass
        self.background = background
        self.stats = self.placeStats()
        self.modifiers = self.calcModifiers()
        self.level = level
        for _ in range(level - 1):
            self.levelUp()
        self.skills = self.calcSkills()
        

    def placeStats(self):
        statArray = generateStatArray()
        #priorityArray = generatePriorityArray(self.class)
        priorityArray = [6, 0, 2, 3, 1, 5] #todo: generatePriorityArray function
        stats = {}

        for _ in range(numStat):
            currPrio = min(priorityArray)
            indexPrio = priorityArray.index(currPrio)
            priorityArray[indexPrio] = numStat + 1 #removing from array would cause indexing issues. This sets the priority above the number of skills, so it will not be reached

            currStat = max(statArray)
            indexStat = statArray.index(currStat)
            statArray[indexStat] = 0 #removing from array would cause indexing issues. This sets the stat to 0, so it will not be reached

            stats[abilities[indexPrio]] = currStat

        if (self.race['stat1id'] != None):
            stats[abilities[self.race['stat1id'] - 1]] += self.race['bonus1']
        
        if (self.race['stat2id'] != None):
            stats[abilities[self.race['stat2id'] - 1]] += self.race['bonus2']

        if (self.race['stat3id'] != None):
            stats[abilities[self.race['stat3id'] - 1]] += self.race['bonus3']
        return stats
    
    def calcModifiers(self):
        modifiers = {}
        for stat in self.stats:
            modifiers[stat] = ((self.stats[stat] // 2) - 5)
        return modifiers

    def calcSkills(self):
        prof = {}
        prof['Acrobatics']      = [0, self.modifiers['Dexterity']]
        prof['Animal Handling'] = [0, self.modifiers['Wisdom']]
        prof['Arcana']          = [0, self.modifiers['Intelligence']]
        prof['Athletics']       = [0, self.modifiers['Strength']]
        prof['Deception']       = [0, self.modifiers['Charisma']]
        prof['History']         = [0, self.modifiers['Intelligence']]
        prof['Insight']         = [0, self.modifiers['Wisdom']]
        prof['Intimidation']    = [0, self.modifiers['Charisma']]
        prof['Investigation']   = [0, self.modifiers['Intelligence']]
        prof['Medicine']        = [0, self.modifiers['Wisdom']]
        prof['Nature']          = [0, self.modifiers['Intelligence']]
        prof['Perception']      = [0, self.modifiers['Wisdom']]
        prof['Performance']     = [0, self.modifiers['Charisma']]
        prof['Persuasion']      = [0, self.modifiers['Charisma']]
        prof['Religion']        = [0, self.modifiers['Intelligence']]
        prof['Sleight of Hand'] = [0, self.modifiers['Dexterity']]
        prof['Stealth']         = [0, self.modifiers['Dexterity']]
        prof['Survival']        = [0, self.modifiers['Wisdom']]
        self.calcProficiencies()
        return prof

    def specialTraits(self):
        name = self.race['name']
        if ('Elf' in name):
            #Darkvision
            #Fey Ancestry
            #Trance
            #Languages
            if ('High' in name):
                #Elf Weapon Training
                #Cantrip
                #Extra language
                pass
            elif ('Wood' in name):
                #Elf Weapon Training
                #Fleet of Foot
                #Mask of the Wild
                pass
            

    def addSkillProficiency(self, skill, proficiency):
        pass

    def addLanguage(self, language):
        pass
    
    def addEquipmentProficiency(self, equipment, proficiency):
        pass

    def levelUp(self):
        self.dndClass.levelUp()
    
    def print(self):
        print(self.race['name'])
        print(self.dndClass, self.level)
        print(self.background)
        print(self.stats)
        print(self.modifiers)
        print(self.skills)
        

def rollStat():
    stats = []
    for i in range(4):
        stats.append(random.randint(1, 6))
    stats.remove(min(stats))
    return sum(stats)


def generateStatArray(): 
    stats = []
    for i in range(numStat):
        stats.append(rollStat())
    return stats

def generatePriorityArray():
    priority = []
    for i in range(numStat):
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

def selectRace():
    pass

def fetchSubraces(race):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jDAN0921",
        auth_plugin='mysql_native_password',
        database='npc_mancer_db'
    )

    mycursor = db.cursor(dictionary=True)
    mycursor.execute("SELECT subrace FROM SUBRACES WHERE ", race)

def getRace(name):
    return list(filter(lambda race : race['name'] == name, playableRaces))[0]


fetchRaces()
steve = Character(getRace("High Elf"), 'ranger', 'urchin', 1)
steve.print()

