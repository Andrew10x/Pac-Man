import math

from settings import *
from player import *
from enemy import *
import pygame
import sys

pygame.init()
vect = pygame.math.Vector2


class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = maze_width // cols
        self.cell_height = maze_height // rows
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.grid = [[0 for x in range(cols)] for x in range(rows)]
        self.p_pos = vect(1, 1)
        self.wall_img = None
        self.load()
        self.player = Player(self, vect(pl_start_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

    def load(self):
        self.background = pygame.image.load('img/black1.jpg')
        self.background = pygame.transform.scale(self.background, (maze_width, maze_height))  ##
        self.wall_img = pygame.transform.scale(pygame.image.load('img/wall.png'), (self.cell_width, self.cell_height))
        self.make_maze()
        # with open('maze2.txt', 'r') as file:
        #    for yidx, line in enumerate(file):
        #        for xidx, char in enumerate(line):
        #            if char == '1':
        #                self.walls.append(vect(xidx, yidx))
        #            elif char == 'c':
        #                self.coins.append(vect(xidx, yidx))
        #            elif char == 'p':
        #                pl_start_pos = vect(xidx, yidx)
        #            elif char in ['2', '3', '4', '5']:
        #                self.e_pos.append(vect(xidx, yidx))
        #            elif char == 'b':
        #                pygame.draw.rect(self.background, (0, 0, 0, 0), (xidx * self.cell_width,
        #                                                                 yidx * self.cell_height,
        #                                                                 self.cell_width, self.cell_height))
        # self.make_maze()

    def make_maze(self):
        unvis_count = 0

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i == 0 or j == 0 or i == len(self.grid) - 1 or j == len(self.grid[i]) - 1:
                    self.grid[i][j] = 1
                elif i % 2 == 1 and j % 2 == 1:
                    self.grid[i][j] = 0
                    unvis_count += 1
                else:
                    self.grid[i][j] = 1

        visited = []
        neighbours = []
        stack = []

        cur = pl_start_pos

        while unvis_count:
            visited.append(cur)

            neighbours = self.get_neighbours(cur, visited)
            if len(neighbours):
                next = self.get_rand_neighbour(neighbours)
                visited.append(next)
                stack.append(cur)
                self.remove_wall(cur, next, self.grid)
                cur = next
                unvis_count -= 1
            elif len(stack):
                cur = stack.pop()

            if unvis_count == 1:
                cent_place = [[-1, -1, -1, -1, -1, -1],
                              [2, -1, -1, -1, -1, 3],
                              [-1, -1, -1, -1, -1, -1],
                              [4, -1, -1, -1, -1, 5]]
                for i in range(len(cent_place)):
                    for j in range(len(cent_place[i])):
                        self.grid[i + 12][j + 11] = cent_place[i][j]
                for i in range(len(self.grid)):
                    if 0 < i < len(self.grid) - 2:
                        self.grid[i][1] = 0
                        self.grid[i][len(self.grid[i]) - 3] = 0
                for j in range(len(self.grid[0])):
                    if 0 < j < len(self.grid[0]) - 2:
                        self.grid[1][j] = 0
                        self.grid[len(self.grid)-3][j] = 0
                break
        self.grid[2][1] = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    self.walls.append(vect(j, i))
                elif self.grid[i][j] == 0:
                    self.coins.append(vect(j, i))
                    self.grid[i][j] = 'c'
                elif self.grid[i][j] == -1:
                    self.grid[i][j] = 0
                elif self.grid[i][j] in [2, 3, 4, 5]:
                    self.e_pos.append(vect(j, i))

    def get_neighbours(self, pos, visited):
        neigh = [vect(pos.x, pos.y + 2), vect(pos.x, pos.y - 2), vect(pos.x + 2, pos.y), vect(pos.x - 2, pos.y)]
        res = []
        for el in neigh:
            if el not in visited:
                if 0 <= el.x < cols - 1 and 0 <= el.y < rows - 1:
                    res.append(el)
        return res

    def get_rand_neighbour(self, neigh):
        index = random.randint(0, len(neigh) - 1)
        return neigh[index]

    def remove_wall(self, cur, next, grid):
        # ?
        x = math.ceil((cur.x + next.x) / 2)
        y = math.ceil((cur.y + next.y) / 2)
        grid[y][x] = 0

    def draw_text(self, screen, size, color, name, text, pos, centered=False):
        font = pygame.font.SysFont(name, size)
        my_text = font.render(text, False, color)
        text_size = my_text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(my_text, pos)

    def draw_grid(self):
        for wall in self.walls:
            self.screen.blit(self.wall_img, (
                wall.x * self.cell_width + self.cell_width + 4, wall.y * self.cell_height + self.cell_height + 4))
            pygame.draw.rect(self.background, (177, 165, 84), (wall.x * self.cell_width, wall.y * self.cell_height,
                                                               self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, pos, idx))
            print(idx)

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.coins = []
        self.player.grid_pos = vect(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_pos = vect(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        #with open('maze.txt', 'r') as file:
        #    for yidx, line in enumerate(file):
        #        for xidx, char in enumerate(line):
        #            if char == 'c':
        #                self.coins.append(vect(xidx, yidx))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'c':
                    self.coins.append(vect(j, i))
        self.state = 'playing'

    def start_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill((0, 0, 0))
        text1 = 'Push space bar'
        text2 = 'One player only'
        pos_tx = maze_width // 2
        pos_ty = maze_height // 2
        self.draw_text(self.screen, start_text_size + 8, (185, 134, 27), font_name, text1, [pos_tx, pos_ty - 20], True)
        self.draw_text(self.screen, start_text_size + 8, (51, 153, 153), font_name, text2, [pos_tx, pos_ty + 50], True)
        pygame.display.update()

    def playing_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    self.player.move(vect(-1, 0))
                if ev.key == pygame.K_RIGHT:
                    self.player.move(vect(1, 0))
                if ev.key == pygame.K_UP:
                    self.player.move(vect(0, -1))
                if ev.key == pygame.K_DOWN:
                    self.player.move(vect(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (25, 25))
        self.draw_coins()
        self.draw_grid()
        self.draw_text(self.screen, start_text_size, (255, 255, 255), font_name, 'current score: {}'
                       .format(self.player.current_score), [25, 0])
        self.draw_text(self.screen, start_text_size, (255, 255, 255), font_name, 'Pac-Man', [width * 3 // 5, 0])
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = 'game over'
        else:
            self.player.grid_pos = vect(self.p_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vect(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (212, 183, 41),
                               (coin.x * self.cell_width + self.cell_width // 2 + side // 2,
                                coin.y * self.cell_height + self.cell_height // 2 + side // 2), 5)

    def game_over_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                self.reset()

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill((0, 0, 0))
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text(self.screen, 52, (255, 10, 15), "arial", "GAME OVER", [width // 2, 100], True)
        self.draw_text(self.screen, 36, (203, 203, 175), "arial", again_text, [width // 2, height // 2], True)
        pygame.display.update()
