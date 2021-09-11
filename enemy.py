import pygame
import random
from settings import *

# vect = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = self.app.cell_width//2.4
        self.number = number
        self.color = self.set_color()
        self.direction = vect(1, 0)
        self.personality = self.set_personality()

    def update(self):
        if self.direction:
            self.pix_pos = self.pix_pos + self.direction
        if self.time_to_move():
            self.move()

        self.grid_pos[0] = (self.pix_pos[0] - side +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - side +
                            self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.radius)

    def time_to_move(self):
        if int(self.pix_pos.x + side // 2) % self.app.cell_width == 0:
            if self.direction == vect(1, 0) or self.direction == vect(-1, 0) or self.direction == vect(0, 0):
                return True
        if int(self.pix_pos.y + side // 2) % self.app.cell_height == 0:
            if self.direction == vect(0, 1) or self.direction == vect(0, -1) or self.direction == vect(0, 0):
                return True
        return False

    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_dir()

    def get_random_dir(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = vect(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vect(x_dir, y_dir)

    def get_pix_pos(self):
        return vect((self.grid_pos.x*self.app.cell_width)+side//2+self.app.cell_width//2,
                    (self.grid_pos.y*self.app.cell_height)+side//2 +
                    self.app.cell_height//2)

    def set_color(self):
        if self.number == 0:
            return 255, 51, 255
        elif self.number == 1:
            return 0, 255, 0
        elif self.number == 2:
            return 0, 204, 204
        elif self.number == 3:
            return 102, 0, 204

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        elif self.number == 3:
            return "scared"