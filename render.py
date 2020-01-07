import pygame
from card2 import Card

TILESIZE = 56

GREEN = (100, 200, 100)
RED = (200, 100, 100)


class Renderer:

    def __init__(self):
        self.tiles = pygame.image.load('img/tiles54.png')
        self.tiles = pygame.transform.scale2x(self.tiles)
        self.img_serail = self.load_image(0,0)
        self.img_garden = self.load_image(1,0)
        self.img_tower = self.load_image(2,0)
        self.img_gemaecher = self.load_image(3, 0)
        self.img_pavillon = self.load_image(0, 1)
        self.img_arkaden = self.load_image(1, 1)
        self.img_empty = self.load_image(2,1)

        self.img_wall_top = self.load_image(0,2)
        self.img_wall_right = self.load_image(1, 2)
        self.img_wall_bottom = self.load_image(2, 2)
        self.img_wall_left = self.load_image(3, 2)

        self.img_hud = pygame.image.load("img/hud54.png")

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 60)

    def render_card(self, window, card, x, y):
        if card.type == Card.TYPE_EMPTY:
            window.blit(self.img_empty, (x, y))
        elif card.type == Card.TYPE_GARDEN:
            window.blit(self.img_garden, (x, y))
        elif card.type == Card.TYPE_SERAIL:
            window.blit(self.img_serail, (x, y))
        elif card.type == Card.TYPE_TOWER:
            window.blit(self.img_tower, (x, y))
        elif card.type == Card.TYPE_GEMAECHER:
            window.blit(self.img_gemaecher, (x, y))
        elif card.type == Card.TYPE_ARKADEN:
            window.blit(self.img_arkaden, (x, y))
        elif card.type == Card.TYPE_PAVILLON:
            window.blit(self.img_pavillon, (x, y))

        if card.walls[0]:
            window.blit(self.img_wall_top, (x, y))
        if card.walls[1]:
            window.blit(self.img_wall_right, (x, y))
        if card.walls[2]:
            window.blit(self.img_wall_bottom, (x, y))
        if card.walls[3]:
            window.blit(self.img_wall_left, (x, y))

    def render(self, window, game, world, shop, reserve, stats):
        x = 0
        for row in world.map:
            y = 0
            for card in row:
                self.render_card(window, card, x, y)
                y += 2*TILESIZE
            x += 2*TILESIZE
        window.blit(self.img_hud, (2*9*TILESIZE, 0))

        for i in range(0, 4):
            self.render_card(window, shop.cards[i], game.shop_slots[i].left, game.shop_slots[i].top)
            price = self.font.render(str(shop.prices[i]) + "€", True, GREEN if stats.money >= shop.prices[i] else RED)
            window.blit(price, (game.shop_slots[i].left, game.shop_slots[i].top + TILESIZE + 60))

        for i in range(0, 4):
            if reserve.cards[i] is not None:
                self.render_card(window, reserve.cards[i], game.reserve_slots[i].left, game.reserve_slots[i].top)

        money = self.font.render(str(stats.money) + "€", True, GREEN)
        window.blit(money, (1040, 630))

        day = self.font.render("Day " + str(stats.day), True, GREEN)
        window.blit(day, (1040, 690))

        pride = self.font.render("Pride: " + str(stats.pride), True, GREEN)
        window.blit(pride, (1040, 750))

        joy = self.font.render("Joy: " + str(stats.joy), True, GREEN)
        window.blit(joy, (1300, 630))

        social = self.font.render("Social: " + str(stats.social), True, GREEN)
        window.blit(social, (1300, 690))

    def load_image(self, x, y):
        img = pygame.Surface((TILESIZE * 2, TILESIZE * 2), pygame.SRCALPHA)
        img.blit(self.tiles, (0, 0), (TILESIZE * 2 * x, TILESIZE * 2 * y, TILESIZE * 2, TILESIZE * 2))
        return img
