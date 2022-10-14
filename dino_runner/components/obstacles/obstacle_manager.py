import pygame
import random

from dino_runner.utils.constants import SHIELD_TYPE
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import BIRD


class ObstacleManager:
    def __init__(self):
        self.Obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(Cactus('LARGE'))
            elif random.randint(0, 2) == 1:
                self.obstacles.append(Cactus('SMALL'))
            elif random.randint(0, 2) == 2:
                self.obstacles.append(Bird(BIRD))
        

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(1000)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    self.obstacles.remove(obstacle)
        

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []