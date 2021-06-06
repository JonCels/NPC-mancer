from enum import Enum

Races = Enum('Races', 'DWARF, ELF, HALFLING, HUMAN, DRAGONBORN, GNOME, HALF-ELF, HALF-ORC, TIEFLING')
Skills = Enum('Skills', 'STRENGTH, DEXTERITY, CONSTITUTION, INTELLIGENCE, WISDOM, CHARISMA')

class Race():
    def __init__(self, name, bonus1, bonus2):
        self.name = name
        self.bonus1 = bonus1
        self.bonus2 = bonus2
        print(bonus1[0].name)
        print(bonus1[1])
        print(bonus2[0].name)
        print(bonus2[1])

DragonBorn = Race(Races.DRAGONBORN, [Skills.STRENGTH, 2], [Skills.CHARISMA, 1])
