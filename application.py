from settings import *
from player import *
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
        self.cell_width = maze_width//28
        self.cell_height = maze_height//30
        self.player = Player(self, pl_start_pos)
        self.walls = []
        self.load()
        
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
            else:
                self.running = False
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (maze_width, maze_height))   ##

        with open('maze.txt', 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vect(xidx, yidx))
        print(self.walls)

    def draw_text(self, screen, size, color, name, text, pos, centered=False):
        font = pygame.font.SysFont(name, size)
        my_text = font.render(text, False, color)
        text_size = my_text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(my_text, pos)

    def draw_grid(self):
        for x in range(maze_width // self.cell_width):
            pygame.draw.line(self.background, (105, 105, 105), (x*self.cell_width, 0), (x*self.cell_width,
                                                                                        maze_height))

        for x in range(maze_height // self.cell_height):
            pygame.draw.line(self.background, (105, 105, 105), (0, x*self.cell_height), (maze_width,
                                                                                         x*self.cell_height))

        for wall in self.walls:
            pygame.draw.rect(self.background, (155, 211, 154), (wall.x*self.cell_width, wall.y*self.cell_height,
                                                               self.cell_width, self.cell_height))

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
        text3 = 'high score'
        pos_tx = maze_width // 2
        pos_ty = maze_height // 2
        self.draw_text(self.screen, start_text_size, (185, 134, 27), font_name, text1, [pos_tx, pos_ty], True)
        self.draw_text(self.screen, start_text_size, (51, 153, 153), font_name, text2, [pos_tx, pos_ty+50], True)
        self.draw_text(self.screen, start_text_size, (242, 243, 222), font_name, text3, [5, 3])
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

    def playing_draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (25, 25))
        self.draw_grid()
        self.draw_text(self.screen, start_text_size, (255, 255, 255), font_name, 'current score: 0', [25, 0])
        self.draw_text(self.screen, start_text_size, (255, 255, 255), font_name, 'high score: 0', [width//2, 0])
        self.player.draw()
        pygame.display.update()




























