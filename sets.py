import pygame


class Sets:
    def __init__(self, game):
        self.game, self.screen = game, game.screen
        self._colors_and_line()
        self._plane_settings()
        self._wall_settings()
        self._get_screen_rect()

    def _colors_and_line(self):
        self.grey = (230, 230, 230)
        self.black = (0, 0, 0)
        self.green = (0, 250, 0)
        self.red = (250, 0, 0)
        self.blue = (0, 0, 250)
        self.line_width = 1

    def _plane_settings(self):
        self.one_point = 10
        self.plane_width, self.plane_height = 4.5 * self.one_point, 1.7 * self.one_point
        # 机身设置
        self.plane_body = [[(0, 0), (1, 0), (1.2, 0.5), (0, 0.5)],
                           [(0, 0.5), (2.5, 0.5), (4.5, 0.85), (2.5, 1.2), (0, 1.2)],
                           [(0, 1.7), (1, 1.7), (1.2, 1.2), (0, 1.2)],
                           [(0, 0.8), (1.2, 0.8), (1.2, 0.9), (0, 0.9)],
                           [(0, 0), (0, 1.7)]]
        # 每个数字都乘上单位长度
        for i in range(len(self.plane_body)):
            points = self.plane_body[i]
            for j in range(len(points)):
                point = points[j]
                x = point[0] * self.one_point
                y = point[1] * self.one_point
                points[j] = (x, y)
        # 尾焰设置
        self.pbf_speed = 0.1
        self.plane_back_fire = [[(-0.8, 0), (-0.2, 0.5)],
                                [(-0.8, 0.7), (-0.2, 0.75)],
                                [(-0.8, 1), (-0.2, 0.95)],
                                [(-0.8, 1.3), (-0.2, 1.2)],
                                [(-0.8, 1.7), (-0.2, 1.4)]]
        for i in range(len(self.plane_back_fire)):
            points = self.plane_back_fire[i]
            for j in range(len(points)):
                point = points[j]
                x = point[0] * self.one_point
                y = point[1] * self.one_point
                points[j] = (x, y)
        #
        #
        # 移动
        self.plane_speed = 0.5
        # 闪烁 -> 表示无敌

    def _wall_settings(self):
        self.one_width = 50
        self.one_height = 50
        self.stone_width = 50
        self.stone_speed = 0.2
        self.get_point_speed = 0.2
        self.direction_choice_speed = 1
        self.road_width_ucl = 5
        self.road_width_lcl = 3


    def _get_screen_rect(self):
        self.scr = self.screen.get_rect()
        self.ucl = 80
        self.lcl = self.scr.height - self.ucl
        self.left_cl = 50
        self.right_cl = self.scr.width - self.left_cl
        self.mid_y = self.ucl + (self.lcl - self.ucl) // 2
        self.mid_x = self.left_cl + (self.right_cl - self.left_cl) // 2
        # 允许生成新的单层wall的线
        self.create_one_wall_line = self.right_cl - self.stone_width

    def update(self):
        self._get_screen_rect()
