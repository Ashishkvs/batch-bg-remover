import os
from PIL import Image

# Input and output folders
input_folder = "output_images"
output_folder = "jpg_images"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".jpg"
        output_path = os.path.join(output_folder, output_filename)

        with Image.open(input_path) as img:
            # Handle transparency: add white background if image has alpha
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # paste using alpha channel
                img = background
            else:
                img = img.convert("RGB")

            img.save(output_path, "JPEG", quality=95)

        print(f"✅ Converted: {filename} -> {output_filename}")
