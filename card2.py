import random


class Card:

    TYPE_EMPTY = 0
    TYPE_SERAIL = 1
    TYPE_GARDEN = 2
    TYPE_TOWER = 3
    TYPE_PAVILLON = 4
    TYPE_ARKADEN = 5
    TYPE_GEMAECHER = 6

    def __init__(self, type = TYPE_EMPTY):
        self.type = type
        self.walls = [False, False, False, False]

    def clone(self):
        copy = Card()
        copy.type = self.type
        copy.walls = self.walls
        return copy

    def randomize(self):
        self.type = random.randint(1, 6)
        walltype = random.randint(0, 13)
        if walltype == 0:
            self.walls = [False, False, False, False]
        elif walltype == 1:
            self.walls = [True, False, False, False]
        elif walltype == 2:
            self.walls = [False, True, False, False]
        elif walltype == 3:
            self.walls = [False, False, True, False]
        elif walltype == 4:
            self.walls = [False, False, False, True]
        elif walltype == 5:
            self.walls = [True, True, False, False]
        elif walltype == 6:
            self.walls = [False, True, True, False]
        elif walltype == 7:
            self.walls = [False, False, True, True]
        elif walltype == 8:
            self.walls = [True, False, False, True]
        elif walltype == 9:
            self.walls = [True, True, True, False]
        elif walltype == 10:
            self.walls = [True, True, False, True]
        elif walltype == 11:
            self.walls = [True, False, True, True]
        elif walltype == 12:
            self.walls = [False, True, True, True]
