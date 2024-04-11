import pygame
from data import COLOR_BOOK


class Shape:
    """Base class for shapes."""
    def __init__(self, window, x, y, size, width, color):
        self.window = window
        self.x = x
        self.y = y
        self.size = size
        self.width = width
        self.color = color


class xShape(Shape):
    def __init__(self, window, x, y, size, width, color=COLOR_BOOK['white'], center=False, is_animation=False):
        super().__init__(window, x, y, size, width, color)
        self.rect = pygame.Rect(x, y, size, size)
        self.is_animation = is_animation
        self.animation_delay = 50
        self.animation_state = 0

        if center:
            self.rect.center = (x, y)

    def draw(self):
        if self.is_animation:
            if self.animation_state == 0:
                pygame.draw.line(self.window, self.color, (self.rect.x + 30, self.rect.y + self.size // 2),
                                 ((self.rect.x + self.size), self.rect.y), self.width)
            elif self.animation_state == 1:
                pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y + self.size),
                                 ((self.rect.x + self.size), self.rect.y), self.width)
            elif self.animation_state == 2:
                pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y + self.size),
                                 ((self.rect.x + self.size), self.rect.y), self.width)
                pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y),
                                 (self.rect.x + self.size - 30, self.rect.y + self.size // 2), self.width)
            else:
                pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y),
                                 (self.rect.x + self.size, self.rect.y + self.size), self.width)
                pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y + self.size),
                                 (self.rect.x + self.size, self.rect.y), self.width)
                return
            self.animation_state += 1
            pygame.time.delay(self.animation_delay)
        else:
            pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y),
                             (self.rect.x + self.size, self.rect.y + self.size), self.width)
            pygame.draw.line(self.window, self.color, (self.rect.x, self.rect.y + self.size),
                             (self.rect.x + self.size, self.rect.y), self.width)


class circleShape(Shape):
    def __init__(self, window, x, y, size, width, color=COLOR_BOOK['white'], is_animation=False):
        super().__init__(window, x, y, size, width, color)
        self.rect = pygame.Rect(x - 40, y - 40, size * 2, size * 2)
        self.is_animation = is_animation
        self.animation_delay = 50
        self.animation_state = 0

    def draw(self):
        if self.is_animation:
            if self.animation_state == 0:
                pygame.draw.circle(self.window,
                                   color=self.color,
                                   center=(self.x, self.y),
                                   radius=self.size, width=self.width, draw_top_right=True)
            elif self.animation_state == 1:
                pygame.draw.circle(self.window,
                                   color=self.color,
                                   center=(self.x, self.y),
                                   radius=self.size, width=self.width, draw_top_right=True, draw_bottom_right=True)
            elif self.animation_state == 2:
                pygame.draw.circle(self.window,
                                   color=self.color,
                                   center=(self.x, self.y),
                                   radius=self.size, width=self.width, draw_top_right=True, draw_bottom_right=True,
                                   draw_bottom_left=True)
            else:
                pygame.draw.circle(self.window,
                                   color=self.color,
                                   center=(self.x, self.y),
                                   radius=self.size, width=self.width)
                return
            self.animation_state += 1
            pygame.time.delay(self.animation_delay)
        else:
            pygame.draw.circle(self.window,
                               color=self.color,
                               center=(self.x, self.y),
                               radius=self.size, width=self.width)


class lineShape:
    def __init__(self, window, start_pos, end_pos, width, direction, color=COLOR_BOOK['white'], animation=False):
        self.window = window
        self.start_pos = list(start_pos)
        self.end_pos = list(end_pos)
        self.current_pos = [self.start_pos[0], self.start_pos[1]]
        self.color = color
        self.width = width
        self.direction = direction
        self.animation = animation

    def draw(self):
        if self.animation:
            if self.current_pos[1] == self.end_pos[1]: # horizontal
                if self.current_pos[0] < self.end_pos[0]:
                    pygame.draw.line(self.window,
                                     start_pos=self.start_pos,
                                     end_pos=self.current_pos,
                                     color=self.color,
                                     width=self.width)
                    self.current_pos[0] += 10
                    return
                else:
                    self.animation = False
            elif self.current_pos[0] == self.end_pos[0]: # vertical
                if self.current_pos[1] < self.end_pos[1]:
                    pygame.draw.line(self.window,
                                     start_pos=self.start_pos,
                                     end_pos=self.current_pos,
                                     color=self.color,
                                     width=self.width)
                    self.current_pos[1] += 10
                    return
                else:
                    self.animation = False
            elif self.current_pos[0] < self.end_pos[0]: # diagonal left to right
                if self.current_pos[1] < self.end_pos[1]:
                    pygame.draw.line(self.window,
                                     start_pos=self.start_pos,
                                     end_pos=self.current_pos,
                                     color=self.color,
                                     width=self.width)
                    self.current_pos[1] += 10
                    self.current_pos[0] += 10
                    return
                else:
                    self.animation = False
            elif self.current_pos[0] > self.end_pos[0]: # diagonal right to left
                if self.current_pos[1] < self.end_pos[1]:
                    pygame.draw.line(self.window,
                                     start_pos=self.start_pos,
                                     end_pos=self.current_pos,
                                     color=self.color,
                                     width=self.width)
                    self.current_pos[0] -= 10
                    self.current_pos[1] += 10
                    return
                else:
                    self.animation = False
        else:
            pygame.draw.line(self.window,
                             start_pos=self.start_pos,
                             end_pos=self.end_pos,
                             color=self.color,
                             width=self.width)


class imageShape:
    def __init__(self, window, image, x, y, width, height):
        self.window = window
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = x
        self.y = y

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))

    def flip(self, x=False, y=False):
        self.image = pygame.transform.flip(self.image, flip_x=x, flip_y=y)
