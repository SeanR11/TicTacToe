import pygame
from text import Text
from data import COLOR_BOOK, get_random_color
from shapes import xShape, circleShape

# Class for creating buttons
class Button:
    def __init__(self, window, x, y, width, height, color=COLOR_BOOK['blue'], function=None, image=None):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.function = function
        if image:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect()

    # Event handler for button events
    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    if self.function:
                        self.function()

    # Method to draw the button
    def draw(self):
        if hasattr(self, 'image'):
            self.window.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(self.window, color=self.color, rect=self.rect)


# Class for creating a rectangular color picker button
class rectColorPicker(Button):
    def __init__(self, window, x, y, width, height, color):
        super().__init__(window, x, y, width, height, color)
        self.title = Text(window=self.window,
                          text='Color',
                          x=self.rect.x + 10, y=self.rect.y - 30,
                          color=COLOR_BOOK['white'],
                          size=30)
        self.clicked = False
        self.function = self.change_color

    # Method to change the color of the button
    def change_color(self):
        random_color = get_random_color()
        while random_color == self.color:
            random_color = get_random_color()
        self.color = random_color
        self.clicked = False


# Class for creating a sign picker button
class SignPicker(Button):
    def __init__(self, window, x, y, default=0):
        super().__init__(window, x, y, 75, 75, function=self.change_sign)
        self.title = Text(window=self.window,
                          text='Sign',
                          x=x + 15, y=y - 30,
                          color=COLOR_BOOK['white'],
                          size=30)
        self.shapes = [xShape(self.window, x, y, 75, 7),
                       circleShape(window=self.window,
                                   y=y + 40, x=x + 40,
                                   size=40, width=5)]
        self.current_shape = self.shapes[default]
        self.rect = self.current_shape.rect
        self.clicked = False
        if default == 0:
            self.sign = 'x'
        else:
            self.sign = 'o'

    # Method to draw the button
    def draw(self):
        self.title.draw()
        self.current_shape.draw()

    # Method to change the sign
    def change_sign(self):
        self.sign = 'o' if self.current_shape == self.shapes[0] else 'x'
        self.current_shape = self.shapes[0] if self.sign == 'x' else self.shapes[1]


# Class for creating an image button
class imageButton(Button):
    def __init__(self, window, image, x, y, width, height, function):
        super().__init__(window, x, y, width, height, image=image, function=function)
        self.color = COLOR_BOOK['lightgrey']
