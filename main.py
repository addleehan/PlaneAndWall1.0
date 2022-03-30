import pygame
import random
import sys
import pygame.font
from sets import Sets
from plane import Plane
from wall import Wall


class ShowGame:
    """显示游戏"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("飞机钻山洞2.0")
        self.sets = Sets(self)
        #
        self.plane = Plane(self)
        self.wall = Wall(self)


    def run(self):
        while True:
            self._get_events()
            self.screen.fill(self.sets.grey)
            self._update_screen()
            pygame.display.update()

    def _update_screen(self):
        self.sets.update()
        self.plane.update()
        self.wall.update()



    def _get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._key_up_events(event)

    def _key_down_events(self, event):
        # move plane
        if event.key == pygame.K_LEFT:
            self.plane.left_move = True
        elif event.key == pygame.K_RIGHT:
            self.plane.right_move = True
        elif event.key == pygame.K_UP:
            self.plane.up_move = True
        elif event.key == pygame.K_DOWN:
            self.plane.down_move = True
        #
        # test
        elif event.key == pygame.K_t:  # for test
            self.plane.shan_up_on_off = not self.plane.shan_up_on_off

    def _key_up_events(self, event):
        if event.key == pygame.K_LEFT:
            self.plane.left_move = False
        elif event.key == pygame.K_RIGHT:
            self.plane.right_move = False
        elif event.key == pygame.K_UP:
            self.plane.up_move = False
        elif event.key == pygame.K_DOWN:
            self.plane.down_move = False


if __name__ == "__main__":
    ai_game = ShowGame()
    ai_game.run()
