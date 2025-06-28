
import os
from PIL import Image

# Configuration
input_folder = "input_images"
output_folder = "output_images"
max_width = 800  # Change as needed
max_height = 800  # Change as needed

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image formats
supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

def resize_image(image_path, output_path, max_w, max_h):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail((max_w, max_h), Image.LANCZOS)  # High-quality downsampling
        img.save(output_path, quality=95)  # Set high quality for output

# Batch processing
for filename in os.listdir(input_folder):
    if filename.lower().endswith(supported_formats):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        resize_image(input_path, output_path, max_width, max_height)
        print(f"Resized: {filename}")

print("All images resized successfully.")
