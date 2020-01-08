import random

class Riot:

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.health = 1

    def move(self, world):
        # riots move randomly for now
        neighbors = [(self.x+1, self.y), (self.x, self.y+1), (self.x-1, self.y), (self.x, self.y-1)]
        target = neighbors[random.randint(0, 3)]
        if world.can_move_riot_to(target):
            self.x = target[0]
            self.y = target[1]
