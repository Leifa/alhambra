import pygame
from render import Renderer
from reserve import Reserve
from world import World
from shop import Shop
from stats import Stats
import config
import random


class Game:

    MODE_IDLE = 0
    MODE_PLACE_CARD = 1

    def __init__(self):
        self.renderer = Renderer()
        self.world = World(config.BOARD_WIDTH, config.BOARD_HEIGHT)
        self.shop = Shop()
        self.shop.randomize_cards()
        self.reserve = Reserve()
        self.stats = Stats()

        self.card_in_placement = None
        self.card_in_placement_cost = 0
        self.mode = Game.MODE_IDLE
        self.shop_slots = [pygame.rect.Rect(1040 + 140 * i, 100, config.TILESIZE, config.TILESIZE) for i in range(0, 4)]
        self.reserve_slots = [pygame.rect.Rect(1040 + 140 * i, 385, config.TILESIZE, config.TILESIZE) for i in range(0, 4)]

        self.running = False

        pygame.display.init()
        self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    def run(self):
        self.running = True
        while self.running:
            pygame.time.wait(30)

            self.handle_events()

            self.window.fill((0, 0, 0))
            self.renderer.render(self.window, self, self.world, self.shop, self.reserve, self.stats)
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if event.button == pygame.BUTTON_RIGHT:
                    self.stats.pride -= 2
                    self.next_turn()
                elif event.button == pygame.BUTTON_LEFT:
                    if self.mode == Game.MODE_IDLE:
                        # Shop Clicked
                        for i in range(0, 4):
                            if self.shop_slots[i].collidepoint(x, y):
                                if self.stats.money >= self.shop.prices[i]:
                                    self.card_in_placement = self.shop.cards[i].clone()
                                    self.card_in_placement_cost = self.shop.prices[i]
                                    self.mode = Game.MODE_PLACE_CARD
                        # Reserve Clicked
                        for i in range(0, 4):
                            if self.reserve_slots[i].collidepoint(x, y):
                                if self.reserve.cards[i] is not None:
                                    self.card_in_placement = self.reserve.cards[i].clone()
                                    self.reserve.cards[i] = None
                                    self.card_in_placement_cost = 0
                                    self.mode = Game.MODE_PLACE_CARD
                    elif self.mode == Game.MODE_PLACE_CARD:
                        bought_card = False
                        for i in range(0, 4):
                            if self.reserve_slots[i].collidepoint(x, y):
                                self.reserve.cards[i] = self.card_in_placement
                                bought_card = True
                        x = x // config.TILESIZE
                        y = y // config.TILESIZE
                        if self.world.does_card_fit(self.card_in_placement, x, y):
                            self.world.set_card(self.card_in_placement, x, y)
                            bought_card = True
                        if bought_card:
                            self.mode = Game.MODE_IDLE
                            self.stats.money -= self.card_in_placement_cost
                            self.stats.pride += 3
                            self.next_turn()

    def next_turn(self):
        self.shop.randomize_cards()
        self.stats.money += 1
        self.stats.money += self.world.get_number_of_arkaden()
        self.stats.day += 1
        self.mode = Game.MODE_IDLE
        self.world.update_riots()
        if random.randint(1, 100) <= self.stats.pride:
            self.world.spawn_riot()

