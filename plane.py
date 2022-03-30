import pygame
from pygame.sprite import Sprite
import time


class Plane(Sprite):
    """飞机"""

    def __init__(self, game):
        super().__init__()
        self.game, self.screen, self.sets = game, game.screen, game.sets
        #
        self.rect = pygame.Rect(0, 0, self.sets.plane_width, self.sets.plane_height)
        self.x, self.y = (self.sets.left_cl, (self.sets.lcl-self.sets.ucl)//2)
        self.left_move = self.right_move = self.up_move = self.down_move = False
        #
        self.back_fire_show_time = time.perf_counter()
        self.back_fire_show_on_off = True
        # 闪烁开关，用来表示无敌
        self.shan_up_on_off = False
        self.show_on_off = True
        self.shan_time = time.perf_counter()

    def update(self):
        # 飞机移动 # 限制移动范围
        if self.left_move and self.x > self.sets.left_cl:
            self.x -= self.sets.plane_speed
        if self.right_move and self.x < self.sets.right_cl:
            self.x += self.sets.plane_speed
        if self.up_move and self.y > self.sets.ucl:
            self.y -= self.sets.plane_speed
        if self.down_move and self.y < self.sets.lcl:
            self.y += self.sets.plane_speed
        # 超过界限，停止
        if self.y <= self.sets.ucl:
            self.y = self.sets.ucl
        elif self.y >= self.sets.lcl:
            self.y = self.sets.lcl
        #
        self.rect.x, self.rect.y = self.x, self.y
        # 变化飞机位置并绘制外形、尾焰
        if time.perf_counter() - self.back_fire_show_time > self.sets.pbf_speed:  # 计时器
            self.back_fire_show_on_off = not self.back_fire_show_on_off
            self.back_fire_show_time = time.perf_counter()
            if self.shan_up_on_off:  # 闪烁开关
                self.show_on_off = self.back_fire_show_on_off
            else:
                self.show_on_off = True
        # 飞机外形绘制，依据显示开关的情况
        if self.show_on_off:
            for i in range(len(self.sets.plane_body)):
                points = self.sets.plane_body[i]
                lis = []
                for j in range(len(points)):
                    point = points[j]
                    x = point[0] + self.rect.x
                    y = point[1] + self.rect.y
                    lis.append((x, y))
                # 绘制多边形     飞机外形
                pygame.draw.polygon(self.screen,
                                    self.sets.black,
                                    lis,
                                    self.sets.line_width)
        # 尾焰开关
        # 变换尾焰位置并根据开关情况绘制
        if self.back_fire_show_on_off:
            for i in range(len(self.sets.plane_back_fire)):
                points = self.sets.plane_back_fire[i]
                lis = []
                for j in range(len(points)):
                    point = points[j]
                    x = point[0] + self.rect.x
                    y = point[1] + self.rect.y
                    lis.append ((x, y))
                # 绘制线 尾焰
                pygame.draw.line(self.screen,
                                 self.sets.black,
                                 lis[0], lis[1],
                                 self.sets.line_width)



