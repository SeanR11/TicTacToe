import pygame
from game import GameFrame
from data import COLOR_BOOK
from player import Player, PC
from text import Text, TextBox
from buttons import rectColorPicker, SignPicker, imageButton


class SetGameFrame:
    def __init__(self, window, parent):
        # Initialize SetGameFrame with window and parent frame
        self.window = window
        self.parent = parent
        self.mode = None
        self.objects = {}
        self.active_objects = {}

    def initialize(self, mode):
        # Initialize the frame with given mode (1P or 2P)
        self.reset_frame()

        # Create title text for the set game screen
        set_game_title = Text(window=self.window, text='Set Game', x=self.parent.width // 2, y=40,
                              center=True, color=COLOR_BOOK['lightblue'], size=75)

        # Create UI elements for player 1 setup
        player_one_label = Text(window=self.window, text='Player 1:', x=150, y=110,
                                center=True, color=COLOR_BOOK['white'], size=60)
        player_one_name_block = TextBox(window=self.window, x=self.parent.width // 2 + 100, y=112,
                                        width=200, height=40, placeholder='enter name', center=True)
        player_one_color_block = rectColorPicker(window=self.window, x=160, y=170,
                                                 width=75, height=75, color=COLOR_BOOK['white'])
        player_one_sign_block = SignPicker(window=self.window, x=320, y=170)

        # Create start game button and return button
        start_game_button = Text(window=self.window, text='Start Game', x=self.parent.width // 2, y=490,
                                 color=COLOR_BOOK['white'], size=60, center=True)
        start_game_button.set_clickable(hover_color=COLOR_BOOK['green'],
                                        function=lambda: self.initialize_game(mode=mode))
        return_button = imageButton(window=self.window, image='assets/return_button.png',
                                    x=12, y=18, width=50, height=50,
                                    function=lambda: self.parent.change_frame('main_menu'))

        # Add UI elements to objects and active_objects dictionaries
        self.objects['title'] = set_game_title
        self.objects['player_one_label'] = player_one_label
        self.active_objects['player_one_nb'] = player_one_name_block
        self.active_objects['player_one_cb'] = player_one_color_block
        self.active_objects['player_one_sb'] = player_one_sign_block
        self.active_objects['return_button'] = return_button
        self.active_objects['start_game_button'] = start_game_button

        if mode == '2P':
            # Create UI elements for player 2 setup if mode is 2P
            player_two_label = Text(window=self.window, text='Player 2:', x=150, y=300,
                                    center=True, color=COLOR_BOOK['white'], size=60)
            player_two_name_block = TextBox(window=self.window, x=self.parent.width // 2 + 100, y=302,
                                            width=200, height=40, placeholder='enter name', center=True)
            player_two_color_block = rectColorPicker(window=self.window, x=160, y=365,
                                                     width=75, height=75, color=COLOR_BOOK['white'])
            player_two_sign_block = SignPicker(window=self.window, x=320, y=365, default=1)

            # Add UI elements for player 2 to objects and active_objects dictionaries
            self.objects['player_two_label'] = player_two_label
            self.active_objects['player_two_nb'] = player_two_name_block
            self.active_objects['player_two_cb'] = player_two_color_block
            self.active_objects['player_two_sb'] = player_two_sign_block

    def event_handler(self, event):
        # Handle events for interactive elements
        for active_obj in self.active_objects.values():
            active_obj.event_handler(event=event)

    def draw(self):
        # Draw UI elements
        mouse_pos = pygame.mouse.get_pos()
        for obj in self.objects.values():
            obj.draw()
        for active_obj in self.active_objects.values():
            active_obj.draw()
            if active_obj.rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def initialize_game(self, mode):
        # Initialize the game with selected parameters
        if self.active_objects['player_one_nb'].text == '':
            self.active_objects['player_one_nb'].text = 'P1'

        player_one = Player(window=self.window,
                            name=self.active_objects['player_one_nb'].text,
                            sign=self.active_objects['player_one_sb'].sign,
                            color=self.active_objects['player_one_cb'].color)
        players = [player_one]
        if mode == '2P':
            # Prepare player objects for 2P mode and create game frame
            if self.active_objects['player_two_nb'].text == '':
                self.active_objects['player_two_nb'].text = 'P2'
            if self.active_objects['player_one_sb'].sign != self.active_objects['player_two_sb'].sign:
                player_two = Player(window=self.window,
                                    name=self.active_objects['player_two_nb'].text,
                                    sign=self.active_objects['player_two_sb'].sign,
                                    color=self.active_objects['player_two_cb'].color)
                players.append(player_two)
            else:
                return
        elif mode == '1P':
            # Create PC player for 1P mode
            player_two = PC(window=self.window,
                            sign=('x' if player_one.sign != 'x' else 'o'))
            players.append(player_two)

        # Create and initialize game frame
        game_frame = GameFrame(window=self.window, parent=self.parent, players=players)
        self.parent.append_frame('game_frame', game_frame)
        self.parent.frames['game_frame'].initialize(mode=mode)
        self.parent.change_frame('game_frame')

    def reset_frame(self):
        # Reset UI elements
        self.objects = {}
        self.active_objects = {}
