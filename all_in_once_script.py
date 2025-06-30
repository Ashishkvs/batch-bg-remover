import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from rembg import remove
from io import BytesIO

# Config
input_folder = "input_images"
output_folder = "output_images"
max_width = 800
max_height = 800

os.makedirs(output_folder, exist_ok=True)

def remove_bg_keep_transparency(image_path):
    with open(image_path, "rb") as f:
        input_bytes = f.read()
    output_bytes = remove(input_bytes)
    return Image.open(BytesIO(output_bytes)).convert("RGBA")

def resize_image(img, max_w, max_h):
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    return img

def apply_food_filter(img: Image.Image):
    # Work on RGB version
    rgb_img = img.convert("RGB")
    cv_img = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)

    # Apply warm tone (red boost, slight green suppress)
    warmth_shift = np.full(cv_img.shape, (10, -3, -10), dtype=np.int16)
    cv_img = np.clip(cv_img.astype(np.int16) + warmth_shift, 0, 255).astype(np.uint8)

    # Convert back to PIL
    rgb_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    # Enhance color vibrance, contrast and sharpness
    rgb_img = ImageEnhance.Color(rgb_img).enhance(1.25)
    rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.05)
    rgb_img = ImageEnhance.Sharpness(rgb_img).enhance(1.1)

    # Re-apply alpha
    alpha = img.getchannel("A")
    final_img = rgb_img.convert("RGBA")
    final_img.putalpha(alpha)
    return final_img

def process_image(file_path, output_path):
    img = remove_bg_keep_transparency(file_path)
    img = resize_image(img, max_width, max_height)
    img = apply_food_filter(img)

    ext = os.path.splitext(output_path)[-1].lower()
    save_params = {}
    if ext == ".png":
        save_params["compress_level"] = 1
    elif ext == ".webp":
        save_params["lossless"] = True
    elif ext in [".jpg", ".jpeg"]:
        save_params["quality"] = 95
        img = img.convert("RGB")  # remove alpha for jpg

    img.save(output_path, **save_params)

# Batch Process
supported_formats = ('.jpg', '.jpeg', '.png', '.webp')
for file in os.listdir(input_folder):
    if file.lower().endswith(supported_formats):
        in_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)
        try:
            process_image(in_path, out_path)
            print(f"✅ Processed: {file}")
        except Exception as e:
            print(f"❌ Error with {file}: {e}")

print("🎯 All food/grocery images processed: background removed, resized, filtered.")
