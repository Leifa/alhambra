import pygame
from render import Renderer
from reserve import Reserve
from world import World
from shop import Shop
from stats import Stats

BLACK = (0, 0, 0)

MODE_IDLE = 0
MODE_PLACE_CARD = 1

TILESIZE = 128

HUD_WIDTH = 704

BOARD_WIDTH = 7
BOARD_HEIGHT = 7

SCREEN_WIDTH = BOARD_WIDTH * TILESIZE + HUD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT * TILESIZE

HUD_LEFT = BOARD_WIDTH * TILESIZE

class Game:

    def __init__(self):
        self.renderer = Renderer()
        self.world = World(BOARD_WIDTH, BOARD_HEIGHT)
        self.shop = Shop()
        self.shop.randomize_cards()
        self.reserve = Reserve()
        self.stats = Stats()
        self.card_in_placement = None
        self.card_in_placement_cost = 0
        self.mode = 0
        self.shop_slots = [pygame.rect.Rect(944 + 160 * i, 100, 128, 128) for i in range(0, 4)]
        self.reserve_slots = [pygame.rect.Rect(944 + 160 * i, 385, 128, 128) for i in range(0, 4)]

        pygame.display.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        running = True
        while running:
            pygame.time.wait(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x = event.pos[0]
                    y = event.pos[1]
                    if event.button == pygame.BUTTON_RIGHT:
                        self.stats.pride -= 2
                        self.next_turn()
                    elif event.button == pygame.BUTTON_LEFT:
                        if self.mode == MODE_IDLE:
                            # Shop Clicked
                            for i in range(0, 4):
                                if self.shop_slots[i].collidepoint(x, y):
                                    if self.stats.money >= self.shop.prices[i]:
                                        self.card_in_placement = self.shop.cards[i].clone()
                                        self.card_in_placement_cost = self.shop.prices[i]
                                        self.mode = MODE_PLACE_CARD
                            # Reserve Clicked
                            for i in range(0, 4):
                                if self.reserve_slots[i].collidepoint(x, y):
                                    if self.reserve.cards[i] is not None:
                                        self.card_in_placement = self.reserve.cards[i].clone()
                                        self.reserve.cards[i] = None
                                        self.card_in_placement_cost = 0
                                        self.mode = MODE_PLACE_CARD
                        elif self.mode == MODE_PLACE_CARD:
                            bought_card = False
                            for i in range(0, 4):
                                if self.reserve_slots[i].collidepoint(x, y):
                                    self.reserve.cards[i] = self.card_in_placement
                                    bought_card = True
                            x = x // 128
                            y = y // 128
                            if self.world.does_card_fit(self.card_in_placement, x, y):
                                self.world.set_card(self.card_in_placement, x, y)
                                bought_card = True
                            if bought_card:
                                self.mode = MODE_IDLE
                                self.stats.money -= self.card_in_placement_cost
                                self.next_turn()

            self.window.fill(BLACK)
            self.renderer.render(self.window, self.world, self.shop, self.reserve, self.stats)
            pygame.display.update()

    def next_turn(self):
        self.shop.randomize_cards()
        self.stats.money += 1
        self.stats.money += self.world.get_number_of_arkaden()
        self.stats.day += 1
        self.mode = MODE_IDLE


game = Game()
game.run()
