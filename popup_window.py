import pygame
from data import COLOR_BOOK

class Popup:
    def __init__(self, window, parent, width, height, bg):
        self.parent = parent
        self.window = window
        self.rect = pygame.Rect(self.parent.width // 2 - width // 2, self.parent.height // 2 - height // 2, width,
                                height)
        self.bg = bg  # Background color of the Popup window
        self.objects = {}  # Dictionary to store non-active objects
        self.active_objects = {}  # Dictionary to store active objects
        self.border = pygame.Rect(self.rect.x - 5, self.rect.y - 5, width + 10, height + 10)  # Border around the Popup window

    def event_handler(self, event):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set default cursor
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        # Handle events for active objects
        for active_obj in self.active_objects.values():
            active_obj.event_handler(event=event)
            if active_obj.rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Set cursor to hand if hovering over clickable object

    def draw(self):
        pygame.draw.rect(self.window, color=COLOR_BOOK['lightblue'], rect=self.border, width=5)  # Draw border
        pygame.draw.rect(self.window, color=self.bg, rect=self.rect)  # Draw background
        for obj in self.objects.values():
            obj.draw()  # Draw non-active objects
        for active_obj in self.active_objects.values():
            active_obj.draw()  # Draw active objects

    def close(self):
        self.parent.frames['game_frame'].reset_game()  # Reset the game when closing the Popup window
