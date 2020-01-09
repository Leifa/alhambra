import random

class Riot:

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.health = 1

    def move(self, world):
        # riots move randomly for now
        neighbors = [(self.x+1, self.y), (self.x, self.y+1), (self.x-1, self.y), (self.x, self.y-1)]
        reachable_neigbors = list(filter(lambda pos: world.can_move_riot_to(self, pos), neighbors))
        distances = []
        for neighbor in reachable_neigbors:
            distances.append(world.distance_to_palace_map[neighbor[0]][neighbor[1]])
        min_distance = min(distances)
        min_distance_neighbors = list(filter(lambda x: world.distance_to_palace_map[x[0]][x[1]] == min_distance, reachable_neigbors))

        target = min_distance_neighbors[random.randint(0, len(min_distance_neighbors)-1)]
        if world.can_move_riot_to(self, target):
            world.move_riot_to(self, target)

    def die(self):
        health = 0
