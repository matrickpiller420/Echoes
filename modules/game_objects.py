import pygame
from abc import ABC, abstractmethod
from modules.settings import UserSettings, DevSettings
import math

class GameObject(ABC):
    def __init__(self, x, y, move_speed):
        self.x = x
        self.y = y
        self.move_speed = move_speed

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class Player(GameObject):
    def __init__(self):
        super().__init__()
        user_settings = UserSettings()
        dev_settings = DevSettings()
        self.look_sensitivity = user_settings.sensitivity
        self.x = dev_settings.player_start_x
        self.y = dev_settings.player_start_y
        self.player_angle =dev_settings.player_start_angle
        self.move_speed = 0.1
        self.handle_input()

    def handle_input(self):
        mouse_dx, _ = pygame.mouse.get_rel()
        self.player_angle += mouse_dx * self.look_sensitivity

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:    # Move forward
            self.x += self.move_speed * math.cos(self.player_angle)
            self.y += self.move_speed * math.sin(self.player_angle)

        if keys[pygame.K_a]:    # Strafe left
            self.x += self.move_speed * math.cos(self.player_angle - (math.pi / 2))
            self.y += self.move_speed * math.sin(self.player_angle - (math.pi / 2))

        if keys[pygame.K_s]:    # Move backward
            self.x -= self.move_speed * math.cos(self.player_angle)
            self.y -= self.move_speed * math.sin(self.player_angle)

        if keys[pygame.K_d]:    # Strafe right
            self.x -= self.move_speed * math.cos(self.player_angle - (math.pi / 2))
            self.y -= self.move_speed * math.sin(self.player_angle - (math.pi / 2))    