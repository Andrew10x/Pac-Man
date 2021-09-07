# from pygame.math import Vector2 as vect
import pygame.draw

from settings import *


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = vect(self.grid_pos.x * self.app.cell_width + side//2 + self.app.cell_width//2,
                            self.grid_pos.y * self.app.cell_height + side//2 + self.app.cell_height//2)
        print(self.grid_pos, self.pix_pos) #
        self.dir = vect(1, 0)

    def update(self):
        self.pix_pos += self.dir

        self.grid_pos[0] = (self.pix_pos[0] - side + self.app.cell_width // 2) // self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1] - side + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, (34, 174, 25), self.pix_pos, self.app.cell_width//2 - 2)

        pygame.draw.rect(self.app.screen, (255, 0, 0), (self.grid_pos[0]*self.app.cell_width + side//2,
                                                        self.grid_pos[1]*self.app.cell_height + side//2,
                                                        self.app.cell_width, self.app.cell_height), 1)

    def move(self, pl_dir):
        self.dir = pl_dir
