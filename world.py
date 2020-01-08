from card2 import Card
import random
from riot import Riot


class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[Card(Card.TYPE_EMPTY) for x in range(0, height)] for y in range(0, width)]
        self.map[4][4] = Card(Card.TYPE_SERAIL)
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
        for riot in self.riots:
            riot.move(self)

    def can_move_riot_to(self, pos):
        if not self.is_in_bounds(pos[0], pos[1]): return False
        if not self.map[pos[0]][pos[1]].type == Card.TYPE_EMPTY: return False
        return True


