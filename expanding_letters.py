import pygame
import sys
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 512, 512
screen = pygame.Surface((width, height))  # Use a Surface instead of setting video mode

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Animation variables
letter_to_animate = "A"  # Change this to animate a different letter
expansion_duration = 3  # Time in seconds for full expansion (adjustable)
fps = 60

# Pre-render the maximum size letter
max_size = max(width, height)
max_font = pygame.font.Font(None, max_size)
max_letter_surface = max_font.render(letter_to_animate, True, WHITE)

class ExpandingLetter:
    def __init__(self, letter):
        self.progress = 0
        self.letter = letter

    def update(self, progress):
        self.progress = progress

    def draw(self, surface):
        size = int(max_size * self.progress)
        if size > 0:
            letter_surface = pygame.transform.smoothscale(max_letter_surface, (size, size))
            letter_rect = letter_surface.get_rect(center=(width // 2, height // 2))
            surface.blit(letter_surface, letter_rect)

# Function to create each frame
def make_frame(t):
    progress = (t % expansion_duration) / expansion_duration
    
    screen.fill(BLACK)
    letter.update(progress)
    letter.draw(screen)
    
    return pygame.surfarray.array3d(screen).swapaxes(0, 1)

# Create the expanding letter object
letter = ExpandingLetter(letter_to_animate)

# Create the video clip
animation = VideoClip(make_frame, duration=expansion_duration)

# Write the video file
video_filename = f'expanding_letter_{letter_to_animate}.mp4'
animation.write_videofile(video_filename, fps=fps)

print(f"Video saved as '{video_filename}'")

# Quit Pygame
pygame.quit()