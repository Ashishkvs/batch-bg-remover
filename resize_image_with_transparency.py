import os
from PIL import Image

# Configuration
input_folder = "input_images"
output_folder = "output_images"
max_width = 800
max_height = 800

# Supported formats
supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def resize_image(input_path, output_path, max_w, max_h):
    with Image.open(input_path) as img:
        # Preserve mode for transparency
        img_format = img.format
        img = img.convert("RGBA") if img.mode in ("P", "LA", "RGBA") else img.convert("RGB")

        # Resize while keeping aspect ratio
        img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Save with proper format and transparency
        save_params = {}
        if img_format == 'PNG':
            save_params["compress_level"] = 1  # Faster compression
        elif img_format == 'WEBP':
            save_params["lossless"] = True
        elif img_format in ['JPEG', 'JPG']:
            save_params["quality"] = 95

        img.save(output_path, format=img_format, **save_params)

# Process each image
for filename in os.listdir(input_folder):
    if filename.lower().endswith(supported_formats):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        resize_image(input_path, output_path, max_width, max_height)
        print(f"Resized: {filename}")

print("All images resized with transparency preserved.")
