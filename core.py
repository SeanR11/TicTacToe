import sys
import pygame
from set_game import SetGameFrame
from main_menu import MainMenuFrame


# core game engine handle the window and frames.
class Core:
    def __init__(self, width, height, title):
        self.window = None
        self.width = width
        self.height = height
        self.title = title
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.is_running = False
        self.frames = {}
        self.active_frame = None
        self.icon = None

    def initialize(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_icon(pygame.image.load('assets/logo.png'))
        pygame.display.set_caption(self.title)
        self.frames['main_menu'] = MainMenuFrame(parent=self, window=self.window)
        self.frames['set_game'] = SetGameFrame(parent=self, window=self.window)
        self.frames['main_menu'].initialize()
        self.change_frame('main_menu')

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            else:
                self.active_frame.event_handler(event=event)

    def draw(self):
        self.window.fill((0, 0, 0))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.active_frame.draw()
        pygame.display.flip()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event_handler()
            self.draw()
            self.clock.tick(self.fps)

    def change_frame(self, frame_name):
        self.active_frame = self.frames[frame_name]

    def append_frame(self, frame_name, frame_object):
        self.frames[frame_name] = frame_object

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    # If this script is run directly, initialize Core object and start the game.
    core = Core(540, 540, 'TicTacToe')
    core.initialize()
    core.run()

