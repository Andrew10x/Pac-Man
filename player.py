import pygame
from settings import *

# vect = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos[0], pos[1]]
        self.grid_pos = vect(pos[0], pos[1])
        self.pix_pos = self.get_pix_pos()
        self.direction = vect(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - side +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - side +
                            self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.app.screen, (230, 250, 70), (int(self.pix_pos.x),
                                                             int(self.pix_pos.y)), self.app.cell_width // 2 - 2)
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, (230, 250, 70), (30 + x*17, height - 15), 7)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if self.time_to_move():
                return True
        else:
            return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vect((self.grid_pos[0] * self.app.cell_width) + side // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   side // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        if int(self.pix_pos.x + side // 2) % self.app.cell_width == 0:
            if self.direction == vect(1, 0) or self.direction == vect(-1, 0) or self.direction == vect(0, 0):
                return True
        if int(self.pix_pos.y + side // 2) % self.app.cell_height == 0:
            if self.direction == vect(0, 1) or self.direction == vect(0, -1) or self.direction == vect(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vect(self.grid_pos + self.direction) == wall:
                return False
        return True
