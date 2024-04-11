import pygame
from text import Text
from data import COLOR_BOOK


class MainMenuFrame:
    def __init__(self, window, parent):
        self.window = window
        self.parent = parent
        self.logo = []  # Array to store logo texts
        self.logo_drawn = False  # Flag to check if the logo has been drawn
        self.active_objects = {}  # Dictionary to store active objects

    def initialize(self):
        # Logo animation setup
        logo_x = 100
        logo_y = 50
        logo_gap = 120
        logo_size = 80
        word_tic = Text(window=self.window,
                        text='TIC',
                        x=(logo_x + (logo_gap * 0)), y=logo_y,
                        color=COLOR_BOOK['green'],
                        size=logo_size)
        word_tac = Text(window=self.window,
                        text='TAC',
                        x=(logo_x + (logo_gap * 1)) - 5, y=logo_y,
                        color=COLOR_BOOK['red'],
                        size=logo_size)
        word_toe = Text(window=self.window,
                        text='TOE',
                        x=(logo_x + (logo_gap * 2)), y=logo_y,
                        color=COLOR_BOOK['blue'],
                        size=logo_size)
        self.logo = [word_tic, word_tac, word_toe]

        # Main menu buttons setup
        one_player_game_button = Text(window=self.window,
                                      text='1 Player',
                                      x=self.parent.width // 2, y=self.parent.height // 2 - 50,
                                      color=COLOR_BOOK['white'],
                                      size=logo_size - 25,
                                      center=True)
        two_player_game_button = Text(window=self.window,
                                      text='2 Players',
                                      x=self.parent.width // 2, y=self.parent.height // 2 + 70,
                                      color=COLOR_BOOK['white'],
                                      size=logo_size - 25,
                                      center=True)
        close_game_button = Text(window=self.window,
                                 text='Close',
                                 x=self.parent.width // 2, y=self.parent.height // 2 + 200,
                                 color=COLOR_BOOK['white'],
                                 size=logo_size - 25,
                                 center=True)

        # Setting click events for buttons
        one_player_game_button.set_clickable(hover_color=COLOR_BOOK['lightblue'],
                                             function=lambda: self.game_setup(mode='1P', frame='set_game'))
        two_player_game_button.set_clickable(hover_color=COLOR_BOOK['lightblue'],
                                             function=lambda: self.game_setup(mode='2P', frame='set_game'))
        close_game_button.set_clickable(hover_color=COLOR_BOOK['lightblue'],
                                        function=lambda: pygame.event.post(pygame.event.Event(256)))

        # Adding buttons to the active objects dictionary
        self.active_objects['1P_game_button'] = one_player_game_button
        self.active_objects['2P_game_button'] = two_player_game_button
        self.active_objects['close_game_button'] = close_game_button

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        for obj in self.active_objects.values():
            obj.event_handler(event=event)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        # Logo animation
        if not self.logo_drawn:
            self.logo_drawn = True
            for word in self.logo:
                word.draw()
                pygame.display.update()
                pygame.time.delay(0)
        else:
            for word in self.logo:
                word.draw()

        # Drawing and handling events for active objects
        for active_obj in self.active_objects.values():
            active_obj.draw()
            if active_obj.rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def game_setup(self, mode, frame):
        self.parent.frames[frame].initialize(mode=mode)
        self.parent.change_frame(frame)
