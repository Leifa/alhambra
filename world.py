from card2 import Card
import random
from riot import Riot


class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[Card(Card.TYPE_EMPTY) for x in range(0, height)] for y in range(0, width)]
        self.map[4][4] = Card(Card.TYPE_SERAIL)
        self.distance_to_palace_map = [[999 for x in range(0, height)] for y in range(0, width)]
        self.calculate_distance_to_palace_map()
        self.riots = []

    def does_card_fit(self, card, x, y):
        # Coordinates out of bounds never fit
        if not self.is_in_bounds(x, y):
            return False
        # The walls must match adjacent cards
        # Must connect to at least one card
        matches_a_neigbor = False
        if self.is_in_bounds(x, y-1):
            if self.map[x][y-1].type != Card.TYPE_EMPTY:
                if self.map[x][y-1].walls[2] != card.walls[0]:
                    return False
                if self.map[x][y-1].walls[2] == False and card.walls[0] == False:
                    matches_a_neigbor = True
        if self.is_in_bounds(x+1, y):
            if self.map[x+1][y].type != Card.TYPE_EMPTY:
                if self.map[x+1][y].walls[3] != card.walls[1]:
                    return False
                if self.map[x+1][y].walls[3] == False and card.walls[1] == False:
                    matches_a_neigbor = True
        if self.is_in_bounds(x, y+1):
            if self.map[x][y+1].type != Card.TYPE_EMPTY:
                if self.map[x][y+1].walls[0] != card.walls[2]:
                    return False
                if self.map[x][y+1].walls[0] == False and card.walls[2] == False:
                    matches_a_neigbor = True
        if self.is_in_bounds(x-1, y):
            if self.map[x-1][y].type != Card.TYPE_EMPTY:
                if self.map[x-1][y].walls[1] != card.walls[3]:
                    return False
                if self.map[x-1][y].walls[1] == False and card.walls[3] == False:
                    matches_a_neigbor = True
        if not matches_a_neigbor:
            return False
        return True

    def is_in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def set_card(self, card, x, y):
        if not self.is_in_bounds(x, y):
            return
        self.map[x][y] = card

    def get_number_of_arkaden(self):
        number = 0
        for row in self.map:
            for card in row:
                if card.type == Card.TYPE_ARKADEN:
                    number += 1
        return number

    def spawn_riot(self):
        corners = [(0, 0), (0, len(self.map)-1), (len(self.map[0])-1, 0), (len(self.map)-1, len(self.map[0])-1)]
        possible_locations = []
        for (x, y) in corners:
            if self.map[x][y].type == Card.TYPE_EMPTY:
                possible_locations.append((x, y))
        i = random.randint(0, len(possible_locations)-1)
        riot = Riot(possible_locations[i])
        self.riots.append(riot)

    def update_riots(self):
        self.riots = [riot for riot in self.riots if riot.health > 0]
        for riot in self.riots:
            riot.move(self)

    def can_move_riot_to(self, riot, pos):
        goal_x = pos[0]
        goal_y = pos[1]

        # if the goal is not adjacent to the riot, return False
        if abs(goal_x - riot.x) + abs(goal_y - riot.y) != 1:
            return False

        # if the goal is out of bounds, return False
        if not self.is_in_bounds(pos[0], pos[1]):
            return False

        # check if walls are inbetween
        if goal_y < riot.y:
            if self.map[goal_x][goal_y].walls[2] or self.map[riot.x][riot.y].walls[0]: return False
        if goal_x > riot.x:
            if self.map[goal_x][goal_y].walls[3] or self.map[riot.x][riot.y].walls[1]: return False
        if goal_y > riot.y:
            if self.map[goal_x][goal_y].walls[0] or self.map[riot.x][riot.y].walls[2]: return False
        if goal_x < riot.x:
            if self.map[goal_x][goal_y].walls[1] or self.map[riot.x][riot.y].walls[3]: return False

        return True

    def move_riot_to(self, riot, target):
        riot.x = target[0]
        riot.y = target[1]
        if self.map[riot.x][riot.y].type != Card.TYPE_EMPTY:
            self.map[riot.x][riot.y] = Card()
            riot.die()
            self.riots.remove(riot)


    def calculate_distance_to_palace_map(self):

        # set all distances to a large number
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.distance_to_palace_map[x][y] = 999

        reachable_locations = []
        done_locations = []

        # mark all palace cards as reachable
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.map[x][y].type != Card.TYPE_EMPTY:
                    if not (x, y) in reachable_locations:
                        reachable_locations.append((x, y))

        while reachable_locations:
            loc = reachable_locations[0]
            x = loc[0]
            y = loc[1]
            card = self.map[x][y]
            if card.type != Card.TYPE_EMPTY:
                # a card of the palace has distance 0 to the palace
                self.distance_to_palace_map[x][y] = 0
                # add neighboring cards to the queue
                if not card.walls[0]:
                    if self.is_in_bounds(x, y-1):
                        if not (x, y-1) in done_locations and not (x, y-1) in reachable_locations:
                            reachable_locations.append((x, y-1))
                if not card.walls[1]:
                    if self.is_in_bounds(x+1, y):
                        if not (x+1, y) in done_locations and not (x+1, y) in reachable_locations:
                            reachable_locations.append((x+1, y))
                if not card.walls[2]:
                    if self.is_in_bounds(x, y+1):
                        if not (x, y+1) in done_locations and not (x, y+1) in reachable_locations:
                            reachable_locations.append((x, y+1))
                if not card.walls[3]:
                    if self.is_in_bounds(x-1, y):
                        if not (x-1, y) in done_locations and not (x-1, y) in reachable_locations:
                            reachable_locations.append((x-1, y))
            else:
                # collect distances of neighbors that do not have a wall towards the current card
                neighbor_distances = []
                if self.is_in_bounds(x, y - 1):
                    if not self.map[x][y-1].walls[2]:
                        neighbor_distances.append(self.distance_to_palace_map[x][y-1])
                if self.is_in_bounds(x+1, y):
                    if not self.map[x+1][y].walls[3]:
                        neighbor_distances.append(self.distance_to_palace_map[x+1][y])
                if self.is_in_bounds(x, y + 1):
                    if not self.map[x][y+1].walls[0]:
                        neighbor_distances.append(self.distance_to_palace_map[x][y+1])
                if self.is_in_bounds(x-1, y):
                    if not self.map[x-1][y].walls[1]:
                        neighbor_distances.append(self.distance_to_palace_map[x-1][y])

                # if we have at least one neighbor, assign distance accordingly
                if neighbor_distances:
                    self.distance_to_palace_map[x][y] = min(neighbor_distances) + 1

                # add all unhandled neighbors to the queue
                if self.is_in_bounds(x, y-1):
                    if not (x, y-1) in done_locations and not (x, y-1) in reachable_locations:
                        reachable_locations.append((x, y-1))
                if self.is_in_bounds(x+1, y):
                    if not (x+1, y) in done_locations and not (x+1, y) in reachable_locations:
                        reachable_locations.append((x+1, y))
                if self.is_in_bounds(x, y+1):
                    if not (x, y+1) in done_locations and not (x, y+1) in reachable_locations:
                        reachable_locations.append((x, y+1))
                if self.is_in_bounds(x-1, y):
                    if not (x-1, y) in done_locations and not (x-1, y) in reachable_locations:
                        reachable_locations.append((x-1, y))

            done_locations.append(reachable_locations.pop(0))







