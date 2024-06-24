import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Expanding Square Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Animation variables
square_size = 0
max_size = min(width, height)
expansion_speed = 2  # Increased to maintain similar visual speed at lower FPS

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill(BLACK)

    # Calculate the position and size of the white square
    square_size = (square_size + expansion_speed) % max_size
    square_pos = (width // 2 - square_size // 2, height // 2 - square_size // 2)

    # Draw the white square
    pygame.draw.rect(screen, WHITE, (*square_pos, square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)  # Changed to 30 FPS

# Quit Pygame
pygame.quit()
sys.exit()