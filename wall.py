import time
import random
import pygame

import sets
from stone import Stone, Road
from pygame.sprite import Sprite


class Wall:
    """点的集合"""
    """重新设置wall，改为建立上、中、下三组点，与road坐标对比，最下、之间、最上的点"""
    """上、下两部分初始设定为两个屏幕以外的点，新点插入二者之间，画多边形"""
    """中间部分，如有，新建点序列，如不再有，序列结束；随时画多边形"""
    """过界时，消除过界的点，保留未过界的点"""
    """"""

    def __init__(self, game):
        self.game, self.screen, self.sets = game, game.screen, game.sets
        #
        self.top_wall = [[self.sets.right_cl, 0]]
        self.bottom_wall = [[self.sets.right_cl, self.sets.lcl]]
        self.walls = [self.top_wall, self.bottom_wall]
        self.get_mid_wall = True
        #

        self.size = [self.sets.road_width_lcl, self.sets.road_width_ucl]
        self.roads = [[self.sets.mid_y, self.sets.lcl], [self.sets.mid_y, self.sets.lcl]]
        self.direction = [0, 0]
        self.choice_time = [time.perf_counter(), time.perf_counter()]
        #
        self.walls_color = self.sets.green
        self.get_point_time = time.perf_counter()

    def update(self):
        # 每一定时间获取一次point
        if time.perf_counter() - self.get_point_time > self.sets.get_point_speed:
            # time zero
            self.get_point_time = time.perf_counter()
            #
            a = self.size[0] * self.sets.plane_height
            b = self.size[1] * self.sets.plane_height
            # 重新提取最后一个点的y坐标
            top0 = self.top_wall[-1][-1]
            bottom0 = self.bottom_wall[-1][-1]
            while True:
                top = random.randint(0, self.sets.lcl)
                bottom = random.randint(0, self.sets.lcl)
                if abs(top - bottom) > a \
                        and abs(top - top0) < a \
                        and abs(bottom - bottom0) < a:
                    top, bottom = min(top, bottom), max(top, bottom)
                    break
            self.top_wall.append([self.sets.right_cl, top])
            self.bottom_wall.append([self.sets.right_cl, bottom])
            # 建立中间墙
            top = int(top + a)
            bottom = int(bottom - a)
            if bottom - top > 5 * a:
                i = 0
                while i < 100:
                    i += 1
                    top = random.randint(top, bottom)
                    bottom = random.randint(top, bottom)
                    if self.get_mid_wall:
                        # 如果没有中间墙，或者上一个墙已经结束, 倒数第二个位置插入一个墙，并且把两个点加入进去
                        # 转为point
                        top = [self.sets.right_cl, top]
                        bottom = [self.sets.right_cl, bottom]
                        self.walls.insert(-1, [top, bottom])
                        self.get_mid_wall = False
                        break
                    else:
                        # 提取点，确认点y坐标波动合格
                        top0 = self.walls[-2][0][-1]
                        bottom0 = self.walls[-2][-1][-1]
                        if abs(top - top0) < a and abs(bottom - bottom0) < a:
                            # 转为point
                            top = [self.sets.right_cl, top]
                            bottom = [self.sets.right_cl, bottom]
                            # 最前、最后分别插入点
                            self.walls[-2].insert(0, top)
                            self.walls[-2].append(bottom)
                            break
            else:
                # 结束墙, 重启
                if self.get_mid_wall is False:
                    self.walls[-2].append('end')
                self.get_mid_wall = True
        # 移动wall
        for wall in self.walls:
            i = 0
            while i < len(wall):
                point = wall[i]
                if point == 'end':
                    break
                point[0] -= self.sets.stone_speed
                # 超出左边界的，删除点
                if point[0] < self.sets.left_cl:
                    wall.pop(i)
                else:
                    i += 1
        # 删掉那些空的中间墙
        i = 1
        while i < len(self.walls) - 1:
            if self.walls[0] == 'end':
                self.walls.pop(i)
            else:
                i += 1
        # 绘制上、下wall的多边形
        for points in self.walls:
            if points == self.walls[0] or points == self.walls[-1]:
                self.walls_color = self.sets.green
            else:
                self.walls_color = self.sets.red
            i = 0
            while i + 1 < len(points):
                point0 = points[i]
                point1 = points[i + 1]
                if point1 == 'end':
                    point1 = points[0]
                pygame.draw.line(self.screen, self.walls_color, point0, point1, self.sets.line_width)
                i += 1



    def _road_update(self):

        for sit in range(len(self.roads)):
            road = self.roads[sit]
            direction = self.direction[sit]
            # 如果计时结束
            if time.perf_counter() - self.choice_time[sit] > self.sets.direction_choice_speed:
                # y坐标随机方向移动
                direction = random.choice((1, -1))
                # 大小随机变化
                size = random.randint(self.size[0], self.size[1])
                height = size * self.sets.stone_width
                road[1] = road[0] + height
                # time zero
                self.choice_time[sit] = time.perf_counter()
            #
            for i in range(len(road)):
                road[i] += self.sets.stone_speed * direction
            # 超过界限，折返
            if road[0] < self.sets.ucl:
                road[0] = self.sets.ucl
                self.direction[sit] = -direction
            elif road[1] > self.sets.lcl:
                road[1] = self.sets.lcl
                self.direction[sit] = -direction
            else:  # 否则，更新
                self.direction[sit] = direction
            # 测试，road
            points = [[self.sets.right_cl, road[0]], [self.sets.right_cl, road[1]]]
            pygame.draw.line(self.screen, self.sets.red, points[0], points[1], self.sets.line_width)
