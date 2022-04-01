import time
import random
import pygame
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
        self.top_wall = []
        self.bottom_wall = []
        self.walls = [self.top_wall, self.bottom_wall]
        #

        self.size = [self.sets.road_width_lcl, self.sets.road_width_ucl]
        self.roads = [[self.sets.mid_y, self.sets.lcl], [self.sets.mid_y, self.sets.lcl]]
        self.direction = [0, 0]
        self.choice_time = [time.perf_counter(), time.perf_counter()]
        #
        self.walls_color = self.sets.green
        self.get_point_time = time.perf_counter()

    def update(self):
        # 随时更新roads
        self._road_update()
        # 获取roads的y坐标的最大值和最小值
        # 每一定时间获取一次
        if time.perf_counter() - self.get_point_time > self.sets.get_point_speed:
            max_y = 0
            min_y = self.sets.scr.height
            for road in self.roads:
                min_y = min(road[0], min_y)
                max_y = max(road[1], max_y)
            # 加入到wall中
            point = [self.sets.right_cl, min_y]
            self.top_wall.append(point)
            point = [self.sets.right_cl, max_y]
            self.bottom_wall.append(point)
            # time zero
            self.get_point_time = time.perf_counter()
        # wall移动
        for wall in self.walls:
            i = 0
            while i < len(wall):
                point = wall[i]
                point[0] -= self.sets.stone_speed
                # 超出左边界的，删除点
                if point[0] < self.sets.left_cl:
                    wall.pop(i)
                else:
                    i += 1
        # 绘制上、下wall的多边形
        top_points = [[self.sets.left_cl, 0]] + self.top_wall + [[self.sets.right_cl, 0]]
        bottom_points = [[self.sets.left_cl, self.sets.lcl]] + self.bottom_wall + [[self.sets.right_cl, self.sets.lcl]]
        # print(top_points)
        for points in [top_points, bottom_points]:
            pygame.draw.polygon(self.screen, self.walls_color, points, self.sets.line_width)

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





