import random
from enum import Enum
import mysql.connector
import math


playableRaces = []
selectableSubraces = []
abilitiesList = []
classesList = []
selectableClassSpecs = []
skillsList = []
backgroundsList = []
armoursList = []

numProf = 18
numStat = 6

selectedRace = {}
selectedSubrace = ""
selectedClass = {}
selectedClassSpec = {}

class Character():
    def __init__(self, race, dndClass, background, level):
        self.race = race[0]['race']
        self.walkSpeed = race[0]['walk_speed']
        self.subrace = race[1]
        self.dndClass = dndClass[0]['class']
        self.dndClassSpec = dndClass[1]['class']
        self.background = background['background']
        self.stats = self.placeStats()
        self.modifiers = self.calcModifiers()
        self.initiative = self.modifiers['Dexterity']
        self.level = level
        for _ in range(level - 1):
            self.levelUp()
        self.skills = self.placeSkills()
        self.proficiencyBonus = self.calcProficiencyBonus()
        self.armour = self.selectArmour("Unarmoured")

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

    #todo
    def generatePriorityArray():
        priority = []
        for i in range(numStat):
            priority.append(i)
        return priority

    def racialTraits(self):
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

    def classTraits(self):
        pass
    
    def backgroundTraits(self):
        pass

    #Adds proficiency in a skill. Pass an optional parameter of 2 for expertise rather than regular proficiency.
    def addSkillProficiency(self, skill, level=1):
        self.skills[skill][0] = level
        self.skills[skill][1] += self.proficiencyBonus * level

    def addLanguage(self, language):
        pass
    
    def addEquipmentProficiency(self, equipment, proficiency):
        pass
    
    def selectArmour(self, armour):
        selectedArmour = getArmour(armour)
        ac = selectedArmour['AC_base']
        mod1 = selectedArmour['AC_mod1']
        mod2 = selectedArmour['AC_mod2']
        ac += self.modifiers[getAbility(mod1)] if mod1 is not None else 0
        ac += self.modifiers[getAbility(mod2)] if mod2 is not None else 0
        self.ac = ac
        return selectedArmour

    def levelUp(self):
        pass
    
    def print(self):
        print(self.race)
        print(self.subrace)
        print(self.dndClassSpec + ",", self.level)
        print(self.background)
        print(self.initiative)
        print(self.walkSpeed)
        print(self.ac)
        print(self.proficiencyBonus)
        print(self.stats)
        print(self.modifiers)
        print(self.skills)
        print(self.armour)
 

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

def fetchAbilities():
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

def fetchClasses():
    db = sqlConnect()

    mycursor = db.cursor(dictionary=True)
    query = "SELECT * FROM classes"
    mycursor.execute(query)

    for dndClass in mycursor:
        classesList.append(dndClass)

#Should be called after selectClass()
def fetchClassSpecs():
    db = sqlConnect()

    selectedClassID = selectedClass['cid']
    mycursor = db.cursor(dictionary=True)
    query = "SELECT class, primaryAbilityID, secondaryAbilityID FROM classspecs WHERE cid =" + str(selectedClassID)
    mycursor.execute(query)

    for classSpec in mycursor:
        selectableClassSpecs.append(classSpec)

def fetchBackgrounds():
    db = sqlConnect()

    mycursor = db.cursor(dictionary=True)
    query = "SELECT background, skillProficiency1ID, skillProficiency2ID FROM backgrounds"
    mycursor.execute(query)

    for background in mycursor:
        backgroundsList.append(background)

def fetchArmours():
    db = sqlConnect()

    mycursor = db.cursor(dictionary=True)
    query = "SELECT name, AC_base, AC_mod1, AC_mod2, classification FROM armour"
    mycursor.execute(query)

    for armour in mycursor:
        armoursList.append(armour)

def sqlConnect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="jDAN0921",
        auth_plugin='mysql_native_password',
        database='npc_mancer_db'
    )
    return db


#Should be called after fetch method for data
def selectRace(race):
    global selectedRace 
    selectedRace = getRace(race)

#Should be called after fetch method for data
def selectSubrace(subrace):
    global selectedSubrace
    selectedSubrace = getSubrace(subrace)

#Should be called after fetch method for data
def selectClass(dndClass):
    global selectedClass
    selectedClass = getClass(dndClass)

#Should be called after fetch method for data
def selectClassSpec(dndClassSpec):
    global selectedClassSpec
    selectedClassSpec = getClassSpec(dndClassSpec)

def selectBackground(background):
    global selectedBackground
    selectedBackground = getBackground(background)

def getRace(name):
    return list(filter(lambda race : race['race'] == name, playableRaces))[0]

def getSubrace(name):
    return list(filter(lambda subrace : subrace['subrace'] == name, selectableSubraces))[0]['subrace']

def getAbility(id):
    return list(filter(lambda ability : ability['aid'] == id, abilitiesList))[0]['ability']

def getClass(name):
    return list(filter(lambda dndClass : dndClass['class'] == name, classesList))[0]

def getClassSpec(name):
    return list(filter(lambda dndClassSpec : dndClassSpec['class'] == name, selectableClassSpecs))[0]

def getBackground(name):
    return list(filter(lambda background : background['background'] == name, backgroundsList))[0]

def getArmour(name):
    return list(filter(lambda armour : armour['name'] == name, armoursList))[0]

fetchAbilities()
fetchSkills()
fetchRaces()
fetchClasses()
fetchBackgrounds()
fetchArmours()

selectRace("Elf")

fetchSubraces()
selectSubrace("High Elf")

selectClass("Ranger")

fetchClassSpecs()
selectClassSpec("Ranger (Dex)")

selectBackground("Urchin")



steve = Character([selectedRace, selectedSubrace], [selectedClass, selectedClassSpec], selectedBackground, 9)
steve.print()


