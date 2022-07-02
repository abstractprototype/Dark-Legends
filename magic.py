import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            # prevents overhealing your hp bar
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles(
                'aura', player.rect.center, groups)
            self.animation_player.create_particles(
                'heal', player.rect.center + pygame.math.Vector2(0, -60), groups)  # the vector2 gives a small particle on top of player

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            # to prevent getting up_idle or up_attack, we only want word before _
            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0, -1)
            else: direction = pygame.math.Vector2(0, 1)  # player.stats.split('_')[0] == 'down':

            for i in range(1, 6):# use i for offset, first element is 1, multiply 1 by tilesize to get offset of 64 pixels to player center
                if direction.x: #horizontal
                    offset_x = (direction.x * i) * TILESIZE # more info on video at 6:15:44
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3) # flames start from center of player, randint to randomize flame graphics 
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x,y), groups)
                else: #vertical
                    offset_y = (direction.y * i) * TILESIZE # more info on video at 6:15:44
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3) # flames start from center of player, randint to randomize flame graphics 
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x,y), groups)