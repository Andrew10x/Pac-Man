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
        self.walk_right = None
        self.walk_left = None
        self.walk_up = None
        self.walk_down = None
        self.anim_count = 0

        self.load()
        self.speed = 2
        self.lives = 3

    def load(self):
        size = self.app.cell_width - 2
        self.walk_right = [pygame.transform.scale(pygame.image.load('img/r1.png'), (size, size)),
                           pygame.transform.scale(pygame.image.load('img/r2.png'), (size, size)),
                           pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]
        self.walk_left = [pygame.transform.scale(pygame.image.load('img/r11.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r21.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]
        self.walk_up = [pygame.transform.scale(pygame.image.load('img/r12.png'), (size, size)),
                        pygame.transform.scale(pygame.image.load('img/r22.png'), (size, size)),
                        pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]
        self.walk_down = [pygame.transform.scale(pygame.image.load('img/r14.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r24.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]

    def update(self):
        if self.anim_count >= 36:
            self.anim_count = 0
        else:
            self.anim_count += 6
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
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
        pac_x = int(self.pix_pos.x - self.app.cell_width//2)
        pac_y = int(self.pix_pos.y - self.app.cell_height//2)
        pac_pos = vect(pac_x, pac_y)
        if self.direction == (0, -1):
            self.app.screen.blit(self.walk_up[self.anim_count // 14], pac_pos)
        elif self.direction == (-1, 0):
            self.app.screen.blit(self.walk_left[self.anim_count // 14], pac_pos)
        elif self.direction == (0, 1):
            self.app.screen.blit(self.walk_down[self.anim_count // 14], pac_pos)
        else:
            self.app.screen.blit(self.walk_right[self.anim_count // 14], pac_pos)
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, (230, 250, 70), (30 + x * 17, height - 15), 7)

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
