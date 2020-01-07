from card2 import Card
import random

class Shop:

    def __init__(self):
        self.cards = [Card() for x in range(0, 4)]
        self.prices = [0, 0, 0, 0]

    def randomize_cards(self):
        for i in range(0, 4):
            while True:
                self.cards[i].randomize()
                card_type_already_appears = False
                for j in range(0, i):
                    if self.cards[j].type == self.cards[i].type:
                        card_type_already_appears = True
                if not card_type_already_appears:
                    break
            num_walls = sum(self.cards[i].walls)
            if num_walls == 3:
                self.prices[i] = random.randint(2, 6)
            elif num_walls == 2:
                self.prices[i] = random.randint(4, 9)
            elif num_walls == 1:
                self.prices[i] = random.randint(6, 12)
            elif num_walls == 0:
                self.prices[i] = random.randint(8, 15)

    def shift_cards(self):
        for i in range(0, 3):
            self.cards[i] = self.cards[i+1].clone()
            self.prices[i] = self.prices[i+1]
        self.cards[3].randomize()
        num_walls = sum(self.cards[3].walls)
        if num_walls == 3:
            self.prices[3] = random.randint(2, 6)
        elif num_walls == 2:
            self.prices[3] = random.randint(4, 9)
        elif num_walls == 1:
            self.prices[3] = random.randint(6, 12)
        elif num_walls == 0:
            self.prices[3] = random.randint(8, 15)

