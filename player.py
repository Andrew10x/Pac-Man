# from pygame.math import Vector2 as vect
import pygame.draw

from settings import *


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()

        print(self.grid_pos, self.pix_pos)  #
        self.dir = vect(1, 0)
        self.stored_direction = None
        self.able_to_move = True

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.dir
        if self.time_to_move():
            if self.stored_direction is not None:
                self.dir = self.stored_direction
        #if self.stored_direction is not None:
        #    self.dir = self.stored_direction  #
        self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - side +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - side +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        print("grid_pos: " + str(self.grid_pos.x) + ':' + str(self.grid_pos.y))

    def draw(self):
        pygame.draw.circle(self.app.screen, (255, 255, 34), (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width // 2 - 2)

        #pygame.draw.rect(self.app.screen, (255, 0, 0), (self.grid_pos[0] * self.app.cell_width + side // 2,
        #                                                self.grid_pos[1] * self.app.cell_height + side // 2,
        #                                                self.app.cell_width, self.app.cell_height), 1)

    def move(self, dir):
        self.stored_direction = dir

    def get_pix_pos(self):
        return vect((self.grid_pos[0]*self.app.cell_width)+side//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   side//2+self.app.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x + side // 2) % self.app.cell_width == 0:
            if self.dir == vect(1, 0) or self.dir == vect(-1, 0) or self.dir == vect(0, 0):
                return True
        if int(self.pix_pos.y + side // 2) % self.app.cell_height == 0:
            if self.dir == vect(0, 1) or self.dir == vect(0, -1) or self.dir == vect(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vect(self.grid_pos + self.dir) == wall:
                return False
        return True
