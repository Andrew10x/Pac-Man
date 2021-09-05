from settings import *
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

    def draw_text(self, screen, size, color, name, text, pos, centered=False):
        font = pygame.font.SysFont(font_name, size, )
        my_text = font.render(text, False, color)
        text_size = my_text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(my_text, pos)

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
        pos_tx = width // 2
        pos_ty = height // 2
        self.draw_text(self.screen, start_text_size, (185, 134, 27), font_name, text1, [pos_tx, pos_ty], True)
        self.draw_text(self.screen, start_text_size, (51, 153, 153), font_name, text2, [pos_tx, pos_ty+50], True)
        self.draw_text(self.screen, start_text_size, (242, 243, 222), font_name, text3, [5, 3])
        pygame.display.update()

    def playing_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        pass

    def playing_draw(self):
        self.screen.fill((37, 213, 149))
        pygame.display.update()




























