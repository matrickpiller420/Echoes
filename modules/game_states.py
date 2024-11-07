import pygame
from abc import ABC, abstractmethod
from modules.button import Button
from modules.gif_animation import GifAnimation
from modules.settings import UserSettings
from modules.game_objects import Player

#### Convert to singleton so can delete state instances when moving to new state
class GameState(ABC):
    def __init__(self):
        self.user_settings = UserSettings()
        self.width, self.height = self.user_settings.resolution
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True

    @abstractmethod
    def handle_events(self):
        """Abstract method to handle events"""
        pass

    @abstractmethod
    def run(self):
        """Abstract method for running the game loop."""
        pass
    
    def quit(self):
        """Clean up when quitting the game state."""
        self.running = False

class MainMenu(GameState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/font/KirangHaerang.ttf", int(self.height / 3))
        self.title_text =  self.font.render("Echoes", True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(int(self.width / 2), int(self.height / 6)))

        button_font_size = 72
        button_font_color = (255,255,255)
        button_font_hover_color = (150,150,150)

        self.new_game_button = Button("New Game", (int(self.width / 2), int(self.height * (4/8))), "assets/font/KirangHaerang.ttf", button_font_size, button_font_color, button_font_hover_color)
        self.continue_button = Button("Continue", (int(self.width / 2), int(self.height * (5/8))), "assets/font/KirangHaerang.ttf", button_font_size, button_font_color, button_font_hover_color)
        self.settings_button = Button("Settings", (int(self.width / 2), int(self.height * (6/8))), "assets/font/KirangHaerang.ttf", button_font_size, button_font_color, button_font_hover_color)
        self.quit_button = Button("Quit Game", (int(self.width / 2), int(self.height * (7/8))), "assets/font/KirangHaerang.ttf", button_font_size, button_font_color, button_font_hover_color)

        self.new_game_animation = GifAnimation(self.screen, "assets/img/gif/loading_maze.gif", 75) # Initialize frames for new game loading gif animation

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif self.new_game_button.is_clicked(event):
                self.screen.fill((0, 0, 0))
                new_game = Game()
                self.run_new_game_animation()
                new_game.run()
                
            # elif self.continue_button.is_clicked(event): # Will be implemented later
            # elif self.settings_button.is_clicked(event):
            elif self.quit_button.is_clicked(event):
                self.running = False  
 
    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill((0, 0, 0))  # Black background

            # Blit title, buttons, etc. to screen
            self.screen.blit(self.title_text, self.title_text.get_rect(center=(int(self.width / 2), int(self.height / 5))))

            self.new_game_button.draw(self.screen)
            self.continue_button.draw(self.screen)
            self.settings_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            pygame.display.flip()   # Update the display
    
    def run_new_game_animation(self):
        # Run new game loading animation loop
        animation_running = True
        while animation_running:
            self.new_game_animation.draw((0, 0))
            pygame.display.flip()

            # Break at last frame
            if self.new_game_animation.frame_index == len(self.new_game_animation.frames) - 1:
                animation_running = False
    
    def quit(self):
        # pygame.mixer.music.stop() or pygame.mixer.quit()
        del self.new_game_animation
        self.running = False

class Game(GameState):
    def __init__(self):
        super().__init__()
        self.map = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]        
        ]
        
        self.player = Player()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True) # lock mouse to window

    # def handle_events(self):

    # def run(self):

    # class Pause(Game):