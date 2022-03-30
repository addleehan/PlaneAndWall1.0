import pygame
from stone import Stone, Road
from pygame.sprite import Sprite


class Wall(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game, self.screen, self.sets = game, game.screen, game.sets
        #
        self.wall = pygame.sprite.Group()
        self.one_wall = pygame.sprite.Group()
        self.roads = pygame.sprite.Group()
        self.stones = {}
        #
        self.road1 = Road(self.game)
        self.road2 = Road(self.game)
        self.roads.add(self.road1, self.road2)
        #
        self.stone_x = self.sets.right_cl
        self.color = self.sets.red

    def update(self):
        pygame.draw.line(self.screen, self.sets.blue,
                         (self.sets.right_cl, 0),
                         (self.sets.right_cl, self.sets.lcl))
        # create a wall
        if len(self.one_wall) < 1:
            i = 0
            y = 0
            while y <= self.sets.lcl:
                stone = Stone(self.game)
                stone.x = self.sets.right_cl
                stone.y = y
                stone.stone_number = i
                stone.left_move = True
                stone.color = self.color
                self.one_wall.add(stone)
                y += stone.rect.height
                i += 1
            # 归零
            self.stone_x = self.sets.right_cl
            #
            if self.color == self.sets.red:
                self.color = self.sets.green
            else:
                self.color = self.sets.red
        # collide roads and be killed
        self.road1.x = self.road2.x = self.sets.right_cl
        self.roads.update()
        pygame.sprite.groupcollide(self.roads, self.one_wall, False, True)
        # other stones add to group
        # 如果石头已经移动了一个身位 ，add, 清空，准备再次生成
        self.stone_x -= self.sets.stone_speed
        if self.stone_x <= self.sets.create_one_wall_line:
            for stone in self.one_wall:
                self.wall.add(stone)
            self.one_wall.empty()
        # 如果越过左边界，kill
        for stone in self.wall:
            if stone.x < self.sets.left_cl:
                stone.kill()
        # 绘制
        pygame.sprite.groupcollide(self.roads, self.wall, False, True)
        self.wall.update()



