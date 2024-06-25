import pygame
import sys
import time
import os
from moviepy.editor import ImageSequenceClip

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 512, 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Overlapping Alternating Expanding Squares")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Animation variables
max_size = min(width, height)
expansion_duration = 3  # Time in seconds for full expansion (adjustable)
expansion_speed = max_size / expansion_duration

class ExpandingSquare:
    def __init__(self, color):
        self.size = 0
        self.color = color

    def update(self, dt):
        self.size += expansion_speed * dt
        return self.size >= max_size

    def draw(self, surface):
        if self.size > 0:
            x = (width - self.size) // 2
            y = (height - self.size) // 2
            pygame.draw.rect(surface, self.color, (x, y, self.size, self.size))

# Create a directory to store frames
if not os.path.exists("frames"):
    os.makedirs("frames")

# Main game loop
clock = pygame.time.Clock()
squares = [ExpandingSquare(WHITE)]  # Start with a white square
last_time = time.time()
frame_count = 0
total_frames = 180  # 3 seconds at 60 fps

# Fill the screen with black initially
screen.fill(BLACK)

while frame_count < total_frames:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    # Update and draw squares
    for square in squares[:]:
        if square.update(dt):
            squares.remove(square)
        square.draw(screen)

    # Start a new square when the last square is halfway
    if squares and squares[-1].size >= max_size / 2 and len(squares) < 2:
        new_color = BLACK if squares[-1].color == WHITE else WHITE
        squares.append(ExpandingSquare(new_color))

    # If all squares are done, start a new white square
    if not squares:
        squares.append(ExpandingSquare(WHITE))

    # Update the display
    pygame.display.flip()

    # Save the frame
    pygame.image.save(screen, f"frames/frame_{frame_count:04d}.png")
    frame_count += 1

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

# Create video from frames
frames = [f"frames/frame_{i:04d}.png" for i in range(total_frames)]
clip = ImageSequenceClip(frames, fps=60)
clip.write_videofile("expanding_squares.mp4")

# Clean up frames
for frame in frames:
    os.remove(frame)
os.rmdir("frames")

print("Video saved as expanding_squares.mp4")