import pygame
from pygame.sprite import Sprite
import random
import time


class Stone(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game, self.screen, self.sets = game, game.screen, game.sets
        #
        self.rect = pygame.Rect(0, 0, self.sets.stone_width, self.sets.one_height)
        #
        self.x = self.sets.right_cl
        self.y = 0
        #
        self.left_move = self.right_move = self.up_move = self.down_move = False
        #
        self.stone_number = 0
        #
        self.color = self.sets.green

    def update(self):
        if self.left_move:
            self.x -= self.sets.stone_speed
        elif self.right_move:
            self.x += self.sets.stone_speed
        elif self.up_move:
            self.y -= self.sets.stone_speed
        elif self.down_move:
            self.y += self.sets.stone_speed
        #
        self.rect.x, self.rect.y = self.x, self.y
        # draw
        pygame.draw.rect(self.screen,
                         self.color,
                         self.rect,
                         self.sets.line_width)


class Road(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game, self.screen, self.sets = game, game.screen, game.sets
        #
        self.rect = pygame.Rect(0, 0, self.sets.one_width, self.sets.one_height)
        #
        self.x = self.sets.right_cl
        self.y = self.sets.mid_y
        #
        self.left_move = self.right_move = self.up_move = self.down_move = False
        #
        self.stone_number = 0
        #
        self.size = [self.sets.road_width_lcl, self.sets.road_width_ucl]
        self.direction = 0
        self.choice_time = time.perf_counter()

    def update(self):
        if time.perf_counter() - self.choice_time > self.sets.direction_choice_speed:
            # y坐标随机方向移动
            self.direction = random.choice((1, -1))
            # 大小随机变化
            size = random.randint(self.size[0], self.size[1])
            self.rect.height = size * self.sets.stone_width
            # time zero
            self.choice_time = time.perf_counter()
        #
        if self.direction < 0:
            self.y -= self.sets.stone_speed
        elif self.direction > 0:
            self.y += self.sets.stone_speed
        # 超过界限，折返
        if self.sets.ucl < self.y < self.sets.lcl:
            pass
        else:
            self.direction = -self.direction
        #
        self.rect.x, self.rect.y = self.x, self.y
        # draw
        pygame.draw.rect(self.screen,
                         self.sets.red,
                         self.rect,
                         self.sets.line_width)
