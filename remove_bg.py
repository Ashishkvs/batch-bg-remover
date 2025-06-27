
import os
from rembg import remove
from PIL import Image

# Define your input and output folders
input_folder = 'input_images'
output_folder = 'output_images'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.png')

        # Open and remove background
        with Image.open(input_path) as img:
            img_no_bg = remove(img)
            img_no_bg.save(output_path)

        print(f'Processed: {filename} -> {output_path}')
