import pygame
from PIL import Image, ImageSequence, ImageOps

class GifAnimation:
    def __init__(self, screen, gif_path, frame_delay):
        self.screen = screen
        self.frames = self.load_gif_frames(gif_path)
        self.frame_delay = frame_delay
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def load_gif_frames(self, gif_path):
        gif = Image.open(gif_path)

        frames = []
        for frame in ImageSequence.Iterator(gif):
            frame = ImageOps.fit(frame, self.screen.get_size())
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()

            # Create a Pygame Surface from the frame data
            image_surface = pygame.image.fromstring(data, size, mode)
            frames.append(image_surface)

        return frames
    
    def draw(self, position):
        time = pygame.time.get_ticks()
        if time - self.last_update > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update = time
            self.screen.blit(self.frames[self.frame_index], position)