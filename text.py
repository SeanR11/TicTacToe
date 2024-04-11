import pygame
from data import COLOR_BOOK


class Text:
    def __init__(self, window, text, x=0, y=0, color=COLOR_BOOK['white'], font='ariel', size=36, bg=COLOR_BOOK['black'],
                 center=False, func=None):
        # initial
        self.window = window
        self.color = color
        self.bg = bg
        self.hover_color = None
        self.font = font
        self.size = size
        self.clickable = False
        self.function = func

        # context represent text displayed on screen and text represent text value
        self.text = text
        self.context = pygame.font.SysFont(self.font, self.size).render(self.text, False, self.color, self.bg)
        self.rect = self.context.get_rect()
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def event_handler(self, event):
        if self.clickable:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.change_color(self.hover_color)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.func()
            else:
                self.change_color(self.color)

    def draw(self):
        self.window.blit(self.context, self.rect)

    def change_color(self, color):
        self.context = pygame.font.SysFont(self.font, self.size).render(self.text, False, color, self.bg)

    def set_clickable(self, hover_color, function):
        self.clickable = True
        self.hover_color = hover_color
        self.func = function


class TextBox:
    def __init__(self, window, x, y, width, height, placeholder, bg=COLOR_BOOK['grey'], center=False):
        self.window = window
        self.surface = pygame.Surface((width, height))
        self.surface.set_alpha(150)
        self.surface.fill(bg)
        self.rect = self.surface.get_rect()
        self.font = pygame.font.SysFont(name='ariel', size=40)
        self.bg = bg
        self.text = ''
        self.placeholder = self.font.render(placeholder, False, COLOR_BOOK['white'])
        self.context = self.font.render(self.text, False, COLOR_BOOK['white'])
        self.focused = False
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos):
                    self.focused = True
                else:
                    self.focused = False
        if event.type == pygame.KEYDOWN:
            if self.focused:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.focused = False
                else:
                    self.text += chr(event.key)
                self.context = self.font.render(self.text, False, COLOR_BOOK['white'])

    def draw(self):
        if self.focused:
            self.surface.set_alpha(255)
            self.surface.fill(self.bg)
        else:
            self.surface.set_alpha(150)

        if self.text == '' and self.focused == False:
            self.surface.blit(self.placeholder, (self.rect.width / 8, 7.5, 0, 0))
        else:
            self.surface.blit(self.context, (10, 7.5, 0, 0))
        self.window.blit(self.surface, (self.rect.x, self.rect.y))
