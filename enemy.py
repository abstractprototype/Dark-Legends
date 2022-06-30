import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats from the dictionary of monster_data
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'./graphics/monsters/{name}/'
        for animation in self.animations.keys():
            # loops through all the animations for the monsters
            # import every image inside that folder to turn it into a surface
            self.animations[animation] = import_folder(main_path + animation)

    # more info from video around 4:35:19
    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        # magnitude converts a vector a distance #the distance alone isn't a "distance"
        distance = (player_vec - enemy_vec).magnitude()

        # just like entity>move function we had to check if direction is not 0, but we have distance for that
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        # the 0 is the distance from get_player_distance_direction return statement
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0  # reset the animation when switching animations
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            print('attack')
        elif self.status == 'move':  # make enemy moves towards the player once the player gets closer
            # the 1 is the direction from get_player_distance_direction return statement
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            # if player moves out of notice radius circle the enemy will stop moving
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':  # stops attacking after attack animation
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
