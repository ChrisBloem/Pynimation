from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import VideoClip
import os

# Animation settings
width, height = 512, 512
letter_to_animate = "A"
expansion_duration = 3  # seconds
fps = 60
total_duration = 6  # Total duration of the animation

# Font selection
def get_font(font_size):
    font_files = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Tahoma.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Times.ttc"
    ]
    
    for font_file in font_files:
        if os.path.exists(font_file):
            return ImageFont.truetype(font_file, font_size)
    
    return ImageFont.load_default()

# Create a base image with the maximum-sized letter
font_size = min(width, height)
font = get_font(font_size)
image = Image.new('RGB', (width, height), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

# Get the size of the letter
left, top, right, bottom = font.getbbox(letter_to_animate)
text_width = right - left
text_height = bottom - top

# Calculate position to center the letter
x = (width - text_width) // 2
y = (height - text_height) // 2 - top  # Adjust for the font's baseline

# Draw the letter
draw.text((x, y), letter_to_animate, font=font, fill=(255, 255, 255))

# Convert to numpy array
letter_array = np.array(image)

class ExpandingLetter:
    def __init__(self, start_time):
        self.start_time = start_time

    def get_size(self, t):
        elapsed = t - self.start_time
        progress = min(1, elapsed / expansion_duration)
        return int(min(width, height) * progress)

def make_frame(t):
    frame = Image.new('RGB', (width, height), color=(0, 0, 0))
    frame_array = np.array(frame)
    
    # Determine which letters should be visible
    visible_letters = [letter for letter in letters if letter.start_time <= t]
    
    for letter in visible_letters:
        size = letter.get_size(t)
        if size > 0:
            resized = Image.fromarray(letter_array).resize((size, size), Image.LANCZOS)
            resized_array = np.array(resized)
            
            # Calculate paste position
            paste_x = (width - size) // 2
            paste_y = (height - size) // 2
            
            # Blend the resized letter with the frame
            frame_array[paste_y:paste_y+size, paste_x:paste_x+size] = np.maximum(
                frame_array[paste_y:paste_y+size, paste_x:paste_x+size],
                resized_array
            )
    
    return frame_array

# Create list of letters with staggered start times
letters = [ExpandingLetter(0)]  # First letter starts immediately
start_time = expansion_duration / 2  # Start time for the second letter
while start_time < total_duration:
    letters.append(ExpandingLetter(start_time))
    start_time += expansion_duration / 2

# Create the video clip
animation = VideoClip(make_frame, duration=total_duration)

# Write the video file
video_filename = f'overlapping_expanding_letters_{letter_to_animate}.mp4'
animation.write_videofile(video_filename, fps=fps)

print(f"Video saved as '{video_filename}'")