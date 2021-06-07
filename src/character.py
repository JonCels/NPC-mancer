import random
from enum import Enum
import mysql.connector
import math

playableClasses = ['Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']

playableBackgrounds = []

playableRaces = []
selectableSubraces = []
abilitiesList = []

savingThrows = abilitiesList

skillsList = []
numProf = 18
numStat = 6

selectedRace = {}
selectedSubrace = {}

class Character():
    def __init__(self, race, subrace, dndClass, background, level):
        self.race = race['race']
        self.walkSpeed = race['walk_speed']
        self.subrace = subrace['subrace']
        self.dndClass = dndClass
        self.background = background
        self.stats = self.placeStats()
        self.modifiers = self.calcModifiers()
        self.level = level
        for _ in range(level - 1):
            self.levelUp()
        self.skills = self.placeSkills()
        self.proficiencyBonus = self.calcProficiencyBonus()

    #Generates an array of ability scores and places them according to common ability priorities based on the character class
    def placeStats(self):
        statArray = generateStatArray()
        #priorityArray = generatePriorityArray(self.class)
        #todo: generatePriorityDict function
        prioDict = {'Strength' : 5, 'Dexterity': 0, 'Constitution': 2, 'Intelligence': 3, 'Wisdom': 1, 'Charisma': 4}
        stats = {}

        for _ in range(numStat):
            #Get next highest priority ability
            currAbility = min(prioDict, key=prioDict.get)
            prioDict.pop(currAbility)
            
            #Get next highest score
            currScore = max(statArray)
            statArray.remove(currScore)

            #Assign score to ability
            stats[currAbility] = currScore
        return stats
    
    def calcModifiers(self):
        modifiers = {}
        for stat in self.stats:
            modifiers[stat] = ((self.stats[stat] // 2) - 5)
        return modifiers

    def placeSkills(self):
        skills = {}
        for skill in skillsList:
            skills[skill[0]] = [0, self.modifiers[getAbility(skill[1])]]
        return skills

    def calcProficiencyBonus(self):
        return math.ceil(1 + (1/4) * self.level)

    

    def specialTraits(self):
        pass
        #name = self.race['name']
        #if ('Elf' in name):
            #Darkvision
            #Fey Ancestry
            #Trance
            #Languages
            #if ('High' in name):
                #Elf Weapon Training
                #Cantrip
                #Extra language
                #pass
            #elif ('Wood' in name):
                #Elf Weapon Training
                #Fleet of Foot
                #Mask of the Wild
                #pass

    #Adds proficiency in a skill. Pass an optional parameter of 2 for expertise rather than regular proficiency.
    def addSkillProficiency(self, skill, level=1):
        self.skills[skill][0] = level
        self.skills[skill][1] += self.proficiencyBonus * level

    def addLanguage(self, language):
        pass
    
    def addEquipmentProficiency(self, equipment, proficiency):
        pass

    def levelUp(self):
        pass
    
    def print(self):
        print(self.race)
        print(self.subrace)
        print(self.dndClass, self.level)
        print(self.background)
        print(self.stats)
        print(self.modifiers)
        print(self.skills)
        print(self.proficiencyBonus)

        

def rollStat():
    stats = []
    for _ in range(4):
        stats.append(random.randint(1, 6))
    stats.remove(min(stats))
    return sum(stats)

def generateStatArray(): 
    stats = []
    for _ in range(numStat):
        stats.append(rollStat())
    return stats

def generatePriorityArray():
    priority = []
    for i in range(numStat):
        priority.append(i)
    return priority

def fetchRaces():
    db = sqlConnect()

    mycursor = db.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM RACES")
    for race in mycursor:
        playableRaces.append(race)

#Should be called after selectRace()
def fetchSubraces():
    db = sqlConnect()

    selectedRaceID = selectedRace['rid']
    mycursor = db.cursor(dictionary=True)
    query = "SELECT subrace FROM subraces WHERE rid =" + str(selectedRaceID)
    mycursor.execute(query)

    for subrace in mycursor:
        selectableSubraces.append(subrace)

def fetchabilitiesList():
    db = sqlConnect()

    mycursor = db.cursor(dictionary=True)
    query = "SELECT * FROM abilities"
    mycursor.execute(query)

    for ability in mycursor:
        abilitiesList.append(ability)

def fetchSkills():
    db = sqlConnect()

    mycursor = db.cursor()
    query = "SELECT skill, abilityID FROM skills"
    mycursor.execute(query)

    for skill in mycursor:
        skillsList.append(skill)
        
def getRace(name):
    return list(filter(lambda race : race['race'] == name, playableRaces))[0]

def getSubrace(name):
    return list(filter(lambda subrace : subrace['subrace'] == name, selectableSubraces))[0]

def getAbility(id):
    return list(filter(lambda ability : ability['aid'] == id, abilitiesList))[0]['ability']

def selectRace(race):
    global selectedRace 
    selectedRace = getRace(race)

def selectSubrace(subrace):
    global selectedSubrace
    selectedSubrace = getSubrace(subrace)

def sqlConnect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jDAN0921",
        auth_plugin='mysql_native_password',
        database='npc_mancer_db'
    )
    return db

fetchabilitiesList()
fetchSkills()

fetchRaces()
selectRace("Elf")

fetchSubraces()
selectSubrace("High Elf")


steve = Character(selectedRace, selectedSubrace, 'ranger', 'urchin', 9)
steve.print()

steve.addSkillProficiency("Religion")
steve.print()

