import pygame

class Button:
    def __init__(self, text, position, font, font_size, color, hover_color):
        self.text = text
        self.position = position
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.hover_color = hover_color

        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(center=self.position)

    def draw(self, screen):
        """Draw button on given screen"""
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            rendered_text = self.font.render(self.text, True, self.color)
        else:
            rendered_text = self.font.render(self.text, True, self.hover_color)

        screen.blit(rendered_text, self.rect.topleft )

    def is_clicked(self, event):
        """Return True if the button clicked, otherwise False"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False