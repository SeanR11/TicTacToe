import pygame
from text import Text
from data import COLOR_BOOK
from popup_window import Popup
from buttons import imageButton
from shapes import lineShape, imageShape

class GameFrame:
    def __init__(self, window, parent, players):
        self.window = window
        self.parent = parent
        self.mode = None
        self.objects = {}
        self.active_objects = {}
        self.players = players
        self.current_player = self.players[0]
        self.winner = None
        self.game_over = False
        self.game_grid = []
        self.game_grid_track = [['', '', ''],
                                ['', '', ''],
                                ['', '', '']]
        self.winning_line = None
        self.popup_window = None

    def initialize(self, mode):
        """
            mode: Game mode ('1P' for single-player, '2P' for two-player).
        """
        self.mode = mode
        # Player labels and signs
        player_one_label = Text(window=self.window,
                                text=self.players[0].name,
                                x=self.parent.width // 4, y=30,
                                center=True,
                                color=self.players[0].color,
                                size=70)
        player_one_sign = self.players[0].shape(x=self.parent.width // 4, y=105, animation=False)

        player_two_label = Text(window=self.window,
                                text=self.players[1].name,
                                x=self.parent.width // 4 * 3, y=30,
                                center=True,
                                color=self.players[1].color,
                                size=60)
        player_two_sign = self.players[1].shape(x=self.parent.width // 4 * 3, y=105, animation=False)

        # Buttons
        return_button = imageButton(window=self.window,
                                    image='assets/return_button.png',
                                    x=12, y=18,
                                    width=50, height=50,
                                    function=lambda: self.parent.change_frame('main_menu'))

        turn_sign = imageShape(window=self.window,
                               image='assets/return_button.png',
                               x=self.parent.width // 2 - 35, y=70,
                               width=70, height=70)

        # Creating game grid
        for row in range(0, 3):
            col_list = []
            for col in range(0, 3):
                col_list.append(GameBlock(window=self.window,
                                          x=97 - (col * 4) + (col * 128), y=166 - (row * 2) + (row * 129)))
            self.game_grid.append(col_list)

        # Adding objects to the dictionary
        self.objects['player_two_label'] = player_two_label
        self.objects['player_two_sign'] = player_two_sign
        self.objects['player_one_label'] = player_one_label
        self.objects['player_one_sign'] = player_one_sign
        self.objects['turn_sign'] = turn_sign

        # Adding active objects
        self.active_objects['return_button'] = return_button

    def event_handler(self, event):
        if self.popup_window is None:
            # Handling game events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    row = 0
                    col = 0
                    for game_blocks in self.game_grid:
                        for block in game_blocks:
                            if block.rect.collidepoint(mouse_pos):
                                if self.mode == '1P' and self.current_player == self.players[1]:
                                    return
                                block.set_sign(
                                    sign_obj=self.current_player.shape(x=block.rect.x + block.rect.width // 2,
                                                                       y=block.rect.y + block.rect.height // 2,
                                                                       animation=True),
                                    sign=self.current_player.sign)

                                self.game_grid_track[row][col] = self.current_player.sign
                                self.objects['turn_sign'].flip(x=True, y=False)
                                self.current_player = self.players[1] if self.current_player == self.players[0] \
                                    else self.players[0]

                            col += 1
                        row += 1
                        col = 0
            # Handling events for active objects
            for active_object in self.active_objects.values():
                active_object.event_handler(event=event)
        else:
            # Handling events for the popup window
            self.popup_window.event_handler(event=event)

        # Handling events for single-player mode
        if self.mode == '1P':
            if event.type == pygame.USEREVENT + 1 and self.players[1].timer:
                self.players[1].timer = False
                self.players[1].ready = True
                return
            if self.current_player == self.players[1] and self.get_empty_cell():
                if self.players[1].ready:
                    self.players[1].make_move(self.game_grid, self.game_grid_track, self.get_empty_cell())
                    self.current_player = self.players[0]
                    self.objects['turn_sign'].flip(x=True, y=False)
                    self.players[1].ready = False
                elif not self.players[1].timer:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                    self.players[1].timer = True

    def draw(self):
        # Drawing objects and active objects
        for obj in self.objects.values():
            obj.draw()

        for active_obj in self.active_objects.values():
            active_obj.draw()

        # Drawing game grid
        for row in self.game_grid:
            for block in row:
                block.draw()

        self.draw_grid()

        # Drawing winning line and handling game over
        if self.game_over:
            if self.winner != 'TIE':
                self.winning_line.draw()
                if not self.winning_line.animation and self.popup_window is None:
                    self.game_over_window()
            else:
                self.game_over_window()
        if self.popup_window is not None:
            self.popup_window.draw()

        # Checking for game over conditions
        if not self.game_over:
            if self.check_for_winner():
                self.game_over = True
            elif not self.get_empty_cell():
                self.game_over = True
                self.winner = 'TIE'

    def draw_grid(self):
        """
        Draws the game grid.
        """
        width = 6
        pygame.draw.line(self.window, COLOR_BOOK['white'], (208, 160), (208, 530), width)
        pygame.draw.line(self.window, COLOR_BOOK['white'], (331, 160), (331, 530), width)
        pygame.draw.line(self.window, COLOR_BOOK['white'], (85, 278), (455, 278), width)
        pygame.draw.line(self.window, COLOR_BOOK['white'], (85, 405), (455, 405), width)

    def get_empty_cell(self):
        """
        Returns a list of empty cells in the game grid.
        """
        return [(row, col) for row in range(3) for col in range(3) if self.game_grid_track[row][col] == '']

    def check_for_winner(self):
        for row in range(0, 3):
            if self.game_grid_track[row][0] == self.game_grid_track[row][1] == self.game_grid_track[row][2] != '':
                self.winning_line = lineShape(window=self.window,
                                              start_pos=self.game_grid[row][0].rect.center,
                                              end_pos=self.game_grid[row][2].rect.center,
                                              width=7,
                                              color=COLOR_BOOK['red'],
                                              direction='col',
                                              animation=True)
                self.set_winner(sign=self.game_grid[row][0].sign)
                return True
            elif self.game_grid_track[0][row] == self.game_grid_track[1][row] == self.game_grid_track[2][row] != '':
                self.winning_line = lineShape(window=self.window,
                                              start_pos=self.game_grid[0][row].rect.center,
                                              end_pos=self.game_grid[2][row].rect.center,
                                              width=7,
                                              color=COLOR_BOOK['red'],
                                              direction='row',
                                              animation=True)
                self.set_winner(sign=self.game_grid[0][row].sign)
                return True
        if self.game_grid_track[0][0] == self.game_grid_track[1][1] == self.game_grid_track[2][2] != '':
            self.winning_line = lineShape(window=self.window,
                                          start_pos=self.game_grid[0][0].rect.center,
                                          end_pos=self.game_grid[2][2].rect.center,
                                          width=7,
                                          color=COLOR_BOOK['red'],
                                          direction='diagLTR',
                                          animation=True)
            self.set_winner(sign=self.game_grid[0][0].sign)
            return True
        elif self.game_grid_track[0][2] == self.game_grid_track[1][1] == self.game_grid_track[2][0] != '':
            self.winning_line = lineShape(window=self.window,
                                          start_pos=self.game_grid[0][2].rect.center,
                                          end_pos=self.game_grid[2][0].rect.center,
                                          width=7,
                                          color=COLOR_BOOK['red'],
                                          direction='diagRTL',
                                          animation=True)
            self.set_winner(sign=self.game_grid[0][2].sign)
            return True
        return False

    def set_winner(self, sign):
        if sign == self.players[0].sign:
            self.winner = self.players[0]
        elif sign == self.players[1].sign:
            self.winner = self.players[1]

    def game_over_window(self):
        """
        Displays the game over window.
        """
        if self.popup_window is None:
            popup = Popup(parent=self.parent,
                          window=self.window,
                          width=360,
                          height=200,
                          bg=COLOR_BOOK['black'])
            winner_label = Text(window=self.window,
                                text=(f'{self.winner.name} is the winner' if self.winner != 'TIE' else 'TIE'),
                                x=popup.rect.x + popup.rect.width // 2, y=popup.rect.y + 30,
                                size=44, center=True,
                                color=COLOR_BOOK['green'])
            play_again_button = Text(window=self.window,
                                     text='Play Again',
                                     x=popup.rect.x + popup.rect.width // 2, y=popup.rect.y + 100,
                                     size=38, center=True)
            menu_button = Text(window=self.window,
                               text='Main Menu',
                               x=popup.rect.x + popup.rect.width // 2, y=popup.rect.y + 160,
                               size=38, center=True)

            play_again_button.set_clickable(hover_color=COLOR_BOOK['lightblue'], function=popup.close)
            menu_button.set_clickable(hover_color=COLOR_BOOK['lightblue'],
                                      function=lambda: self.parent.change_frame('main_menu'))

            popup.objects['winner_label'] = winner_label
            popup.active_objects['play_again_button'] = play_again_button
            popup.active_objects['menu_button'] = menu_button

            pygame.time.delay(300)
            self.popup_window = popup

    def reset_game(self):
        self.objects = {}
        self.active_objects = {}
        self.current_player = self.players[0]
        self.winner = None
        self.game_over = False
        self.game_grid = []
        self.game_grid_track = [['', '', ''],
                                ['', '', ''],
                                ['', '', '']]
        self.winning_line = None
        self.popup_window = None
        self.initialize(mode=self.mode)


class GameBlock:
    def __init__(self, window, x, y, color=COLOR_BOOK['black']):
        self.window = window
        self.rect = pygame.rect.Rect(x, y, 100, 100)
        self.color = color
        self.sign = None
        self.sign_obj = None

    def draw(self):
        if self.sign_obj:
            self.sign_obj.draw()
        else:
            pygame.draw.rect(self.window, self.color, self.rect)

    def set_sign(self, sign_obj, sign):
        self.sign_obj = sign_obj
        self.sign = sign
