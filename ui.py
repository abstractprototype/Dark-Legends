import pygame
from settings import *


class UI:
    def __init__(self):

        # general info
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        # takes the left, top, width, height
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat tp pixel
        ratio = current / max_amount  # 100 / 100 = 1
        current_width = bg_rect.width * ratio  # 200 * 1 = 200
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        # pygame.draw.rect(self.display_surface,
        #                  UI_BORDER_COLOR, current_rect, 3)  # draws a border color around the current health/energy rectangles only
        pygame.draw.rect(self.display_surface,
                         UI_BORDER_COLOR, bg_rect, 3)  # draws a border color around the total health/energy rectangle

    def show_exp(self, exp):
        # takes in info, AntiAliasing(AA), color
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)

        text_rect = text_surf.get_rect(bottomright=(x, y))

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp()
