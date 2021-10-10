import pygame
import random
from settings import *


# vect = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = self.app.cell_width // 2.4
        self.number = number
        self.color = self.set_color()
        self.direction = vect(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.shortest = []
        self.starting_pos = [pos.x, pos.y]
        self.speed = self.set_speed()
        self.image = self.load_img()

    def update(self):

        self.target = self.set_target()
        if self.target != self.grid_pos:
            if self.direction:
                self.pix_pos = self.pix_pos + self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - side +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - side +
                            self.app.cell_height // 2) // self.app.cell_height + 1

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos.x > cols // 2 and self.app.player.grid_pos.y > rows // 2:
                return vect(1, 1)
            if self.app.player.grid_pos.x > cols // 2 and self.app.player.grid_pos.y < rows // 2:
                return vect(1, rows - 3)
            if self.app.player.grid_pos.x < cols // 2 and self.app.player.grid_pos.y > rows // 2:
                return vect(cols - 3, 1)
            else:
                return vect(cols - 3, rows - 3)

    def draw(self):
        #pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.radius)
        self.app.screen.blit(self.image, (self.pix_pos.x - 12, self.pix_pos.y - 12))

        for cell in self.shortest:
           if cell != self.shortest[0] and cell != self.shortest[len(self.shortest) - 1]:
            pygame.draw.rect(self.app.screen,  self.color,
                             (self.get_pix_pos2(cell).x - self.app.cell_width//2,  self.get_pix_pos2(cell).y - self.app.cell_height//2,
                              self.app.cell_width, self.app.cell_height), 1)
        #if self.shortest:
        #    pygame.draw.rect(self.app.background, (177, 165, 84),
        #                     (self.shortest[0][0] * self.app.cell_width, self.shortest[0][1] * self.app.cell_height,
        #                     self.app.cell_width, self.app.cell_height), 1)

    def set_speed(self):
        if self.personality == 'speedy':
            speed = 2
        else:
            speed = 1
        return speed

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
        elif self.personality == 'slow':
            self.direction = self.get_path_dir(self.target)
            #self.direction = self.get_random_dir()
        elif self.personality == 'speedy':
            self.direction = self.get_path_dir(self.target)
            # self.direction = self.get_random_dir()
        elif self.personality == 'scared':
            #self.direction = self.get_path_dir(self.target)
            self.direction = self.get_random_dir()

    def get_path_dir(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vect(x_dir, y_dir)

    def draw_short_path(self, shortest):
        print("Path")
        for cell in shortest:
            print(str(cell[0]) + ":" + str(cell[1]), end=' ')
            pygame.draw.rect(self.app.background, (177, 165, 84),
                             (cell[0] * self.app.cell_width, cell[1] * self.app.cell_height,
                              self.app.cell_width, self.app.cell_height), 0)
        print()

    def find_next_cell_in_path(self, target):
        path = self.BFS([self.grid_pos.x, self.grid_pos.y], [target.x, target.y])
        next_cell = path[1]
        return next_cell

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + current[0] < len(grid[0]):
                        if 0 <= neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[int(next_cell[1])][int(next_cell[0])] != 1:
                                    if next_cell not in queue:
                                        queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        self.shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    self.shortest.insert(0, step["Current"])
        # self.draw_short_path(sefshortest)
        return self.shortest

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
        return vect((self.grid_pos.x * self.app.cell_width) + side // 2 + self.app.cell_width // 2,
                    (self.grid_pos.y * self.app.cell_height) + side // 2 +
                    self.app.cell_height // 2)

    def get_pix_pos2(self, grid_pos):
        return vect((grid_pos[0] * self.app.cell_width) + side // 2 + self.app.cell_width // 2,
                    (grid_pos[1] * self.app.cell_height) + side // 2 +
                    self.app.cell_height // 2)

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

    def load_img(self):
        if self.number == 0:
            return pygame.transform.scale(pygame.image.load('img/Blinky.png'), (24, 24))
        elif self.number == 1:
            return pygame.transform.scale(pygame.image.load('img/Inky.png'), (24, 24))
        elif self.number == 2:
            return pygame.transform.scale(pygame.image.load('img/Pinky.png'), (24, 24))
        elif self.number == 3:
            return pygame.transform.scale(pygame.image.load('img/Clyde.png'), (24, 24))
