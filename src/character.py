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
weaponsList = []

numProf = 18
numStat = 6

selectedRace = {}
selectedSubrace = ""
selectedClass = {}
selectedClassSpec = {}
selectedBackground = {}

class Character():
    def __init__(self, race, dndClass, background, level):
        self.race = race[0]['race']
        self.subrace = race[1]
        self.dndClass = dndClass[0]['class']
        self.dndClassSpec = dndClass[1]['class']
        self.subclass = self.selectSubclass(dndClass)
        #subclass
        self.background = background['background']
        self.level = level
        
        self.prioDict = {}
        self.stats = self.placeStats()
        self.racialTraits()
        self.modifiers = self.calcModifiers()

        self.skills = self.placeSkills()
        self.savingThrows = self.placeSavingThrows()

        self.proficiencyBonus = self.calcProficiencyBonus()
        self.selectArmour("Unarmoured")
        self.initiative = self.modifiers['Dexterity']
        self.walkSpeed = race[0]['walk_speed']
        self.passivePerception = self.calcPassivePerception()

        self.hitDice = dndClass[0]['hit_dice']
        self.hp = self.calcHP()
        self.numHitDice = self.level

        self.backgroundTraits(background)
        self.classTraits(dndClass)

        self.weapons = []

    def selectSubclass(self, dndClass):
        pass

    #Generates an array of ability scores and places them according to common ability priorities based on the character class
    def placeStats(self):
        statArray = generateStatArray()
        #priorityArray = generatePriorityArray(self.class)
        #todo: generatePriorityDict function
        self.prioDict = {'Strength' : 5, 'Dexterity': 0, 'Constitution': 2, 'Intelligence': 3, 'Wisdom': 1, 'Charisma': 4}
        prioDict = self.prioDict.copy()
        stats = {}

        for _ in range(numStat):
            #Get next highest priority ability
            currAbility = min(prioDict, key=prioDict.get)
            prioDict.pop(currAbility)
            
            #Get next highest scores
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
            skills[skill['skill']] = [0, self.modifiers[getAbility(skill['abilityID'])]]
        return skills

    def placeSavingThrows(self):
        savingThrows = {}
        for savingThrow in abilitiesList:
            savingThrows[savingThrow['ability']] = [0, self.modifiers[savingThrow['ability']]]
        return savingThrows

    def calcProficiencyBonus(self):
        return math.ceil(1 + (1/4) * self.level)

    def calcPassivePerception(self):
        self.passivePerception = 10 + self.skills['Perception'][1]

    def calcHP(self):
        #hp = hit dice value + constitution
        hp = self.hitDice + self.modifiers['Constitution']
        return hp

    def addHP(self, hp):
        self.hp += hp

    def levelUp(self):
        #Add any ASI's taken
        lvlHp = random.randint(1, self.hitDice) + self.modifiers['Constitution']
        self.addHP(lvlHp)
        
    #todo
    def generatePriorityArray():
        priority = []
        for i in range(numStat):
            priority.append(i)
        return priority

    def racialTraits(self):
        if (self.race == "Aarakocra"):
            self.stats['Dexterity'] += 2
            self.stats['Wisdom'] += 1
            #Flight
            #Talons
            #Languages

        elif (self.race == "Aasimar"):
            self.stats['Charisma'] += 2
            #Darkvision
            #Celestial Resistance
            #Healing Hands
            #Light Bearer
            #Languages
            if (self.subrace == "Protector Aasimar"):
                self.stats['Wisdom'] += 1
                #Radiant soul
            elif (self.subrace == "Scourge Aasimar"):
                self.stats['Constitution'] += 1
                #Radiant consumption
            elif (self.subrace == "Fallen Aasimar"):
                self.stats['Strength'] += 1
                #Necrotic shroud
        
        elif (self.race == "Bugbear"):
            self.stats['Strength'] += 2
            self.stats['Dexterity'] += 1
            #Darkvision
            #Long limbed
            #Powerful build
            #Sneaky
            #Surprise attack
            #Languages
        
        elif (self.race == "Dragonborn"):
            self.stats['Strength'] += 2
            self.stats['Charisma'] += 1
            #Draconic ancestry
            #Breath weapon
            #Damage resistance
            #Languages

        elif (self.race == "Dwarf"):
            self.stats['Constitution'] += 2
            #Darkvision
            #Dwarven resilience
            #Dwarven combat training
            #Tool proficicency
            #Stonecunning
            #Languages

            if (self.subrace == "Hill Dwarf"):
                self.stats['Wisdom'] += 1
                #Dwarven toughness

            elif (self.subrace == "Mountain Dwarf"):
                self.stats['Strength'] += 2
                #Dwarven armor training

        elif (self.race == "Elf"):
            self.stats['Dexterity'] += 2
            #Darkvision
            #Keen senses
            #Fey ancestry
            #Trance
            #Languages

            if (self.subrace == "High Elf"):
                self.stats['Intelligence'] += 1
                #Elf weapon training
                #Cantrip
                #Extra language

            elif (self.subrace == "Wood Elf"):
                self.stats['Wisdom'] += 1
                #Elf weapon training
                #Fleet of foot
                #Mask of the wild
        
        elif (self.race == "Firbolg"):
            self.stats['Wisdom'] += 2
            self.stats['Strength'] += 1
            #Firbolg magic
            #Hidden step
            #Powerful build
            #Speech of beast and leaf
            #Languages
        
        elif (self.race == "Genasi"):
            self.stats['Constitution'] += 2
            #Languages

            if (self.subrace == "Air Genasi"):
                self.stats['Dexterity'] += 1
                #Unending breath
                #Mingle with the wind
            
            elif (self.subrace == "Earth Genasi"):
                self.stats['Strength'] += 1
                #Earth walk
                #Merge with stone
            
            elif (self.subrace == "Fire Genasi"):
                self.stats['Intelligence'] += 1
                #Darkvision
                #Fire resistance
                #Reach to the blaze

            elif (self.subrace == "Water Genasi"):
                self.stats['Wisdom'] += 1
                #Acid Resistance
                #Amphibious
                #Swim
                #Call to the wave
        
        elif (self.race == "Gnome"):
            self.stats['Intelligence'] += 2
            #Darkvision
            #Gnome cunning
            #Languages

            if (self.subrace == "Forest Gnome"):
                self.stats['Dexterity'] += 1
                #Natural Illusionist
                #Speak with small beasts
            
            elif (self.subrace == "Rock Gnome"):
                self.stats['Constitution'] += 1
                #Artificers lore
                #Tinker
            
            elif (self.subrace == "Deep Gnome"):
                self.stats['Dexterity']
                #Superior darkvision
                #Stone camouflage
        
        elif (self.race == "Goblin"):
            self.stats['Dexterity'] += 2
            self.stats['Constitution'] += 1
            #Darkvision
            #Fury of the small
            #Nimble escape
            #Languages
        
        elif (self.race == "Goliath"):
            self.stats['Strength'] += 2
            self.stats['Constitution'] += 1
            #Natural athlete
            #Stone's endurance
            #Powerful build
            #Mountain born
        
        elif (self.race == "Half-Elf"):
            self.stats['Charisma'] += 2

            #Choose based on abilityPriority
            prioDict = self.prioDict.copy()
            prioDict.pop("Charisma")

            sortedPrioDict = dict(sorted(prioDict.items(), key=lambda item: item[1]))
            focus1 = list(sortedPrioDict.items())[:1][0][0]
            focus2 = list(sortedPrioDict.items())[1:2][0][0]
            self.stats[focus1] += 1
            self.stats[focus2] += 1
        
        elif (self.race == "Half-Orc"):
            self.stats['Strength'] += 2
            self.stats['Constitution'] += 1
            #Darkvision
            #Menacing
            #Relentless endurance
            #Savage attacks
            #Languages
        
        elif (self.race == "Halfling"):
            self.stats['Dexterity'] += 2
            
            if (self.subrace == "Lightfoot Halfling"):
                self.stats['Charisma'] += 1
                #Naturally stealthy
            
            elif (self.subrace == "Stout Halfling"):
                self.stats['Constitution'] += 1
                #Stout resilience
        
        elif (self.race == "Hobgoblin"):
            self.stats['Constitution'] += 2
            self.stats['Intelligence'] += 1
            #Darkvision
            #Martial Training
            #Saving face
            #Languages
            







    def classTraits(self, dndClass):
        #Saving throw proficiencies
        savingThrow1 = getAbility(dndClass[0]['saving_throw_1'])
        savingThrow2 = getAbility(dndClass[0]['saving_throw_2'])
        self.addSavingThrowProficiency(savingThrow1)
        self.addSavingThrowProficiency(savingThrow2)

    def backgroundTraits(self, background):
        #Skill proficiencies
        skill1 = getSkill(background['skillProficiency1ID'])
        skill2 = getSkill(background['skillProficiency2ID'])
        self.addSkillProficiency(skill1)
        self.addSkillProficiency(skill2)

    #Adds proficiency in a skill. Pass an optional parameter of 2 for expertise rather than regular proficiency.
    def addSkillProficiency(self, skill, level=1):
        self.skills[skill][0] = level
        self.skills[skill][1] += self.proficiencyBonus * level
        if (skill == "Perception"):
            self.calcPassivePerception()

    def addSavingThrowProficiency(self, savingThrow):
        self.savingThrows[savingThrow][0] = 1
        self.savingThrows[savingThrow][1] += self.proficiencyBonus

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
        self.armour = selectedArmour
        return selectedArmour

    def selectWeapon(self, weapon):
        selectedWeapon = getWeapon(weapon)
        self.weapons.append(selectedWeapon)

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
        print(self.savingThrows)
        print(self.armour)
        print(self.passivePerception)
        print(self.hitDice)
        print(self.hp)
 

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

    mycursor = db.cursor(dictionary=True)
    query = "SELECT * FROM skills"
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

def fetchWeapons():
    db = sqlConnect()

    mycursor = db.cursor(dictionary=True)
    query = "SELECT name, rolls, damage, damage_type, weapon_type, weapon_range, properties FROM weapons"
    mycursor.execute(query)

    for weapon in mycursor:
        weaponsList.append(weapon)

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

def getSkill(id):
    return list(filter(lambda skill : skill['sid'] == id, skillsList))[0]['skill']

def getClass(name):
    return list(filter(lambda dndClass : dndClass['class'] == name, classesList))[0]

def getClassSpec(name):
    return list(filter(lambda dndClassSpec : dndClassSpec['class'] == name, selectableClassSpecs))[0]

def getBackground(name):
    return list(filter(lambda background : background['background'] == name, backgroundsList))[0]

def getArmour(name):
    return list(filter(lambda armour : armour['name'] == name, armoursList))[0]

def getWeapon(name):
    return list(filter(lambda weapon : weapon['name'] == name, weaponsList))[0]

fetchAbilities()
fetchSkills()
fetchRaces()
fetchClasses()
fetchBackgrounds()
fetchArmours()
fetchWeapons()

selectRace("Half-Elf")

fetchSubraces()
#selectSubrace("Wood Elf")

selectClass("Ranger")

fetchClassSpecs()
selectClassSpec("Ranger (Dex)")

selectBackground("Urchin")

steve = Character([selectedRace, selectedSubrace], [selectedClass, selectedClassSpec], selectedBackground, 9)
steve.addSkillProficiency("Perception")
steve.print()


