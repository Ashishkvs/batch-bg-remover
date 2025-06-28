import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

input_folder = "input_images"
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

def apply_food_filter(image_path, output_path):
    img = Image.open(image_path)
    img_format = img.format

    # Preserve transparency
    img = Image.open(image_path)
    img_format = img.format

    # Detect and safely extract alpha
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info)
    if has_alpha:
        img = img.convert("RGBA")
        alpha = img.getchannel("A")
        img = img.convert("RGB")
    else:
        alpha = None

    # Convert to OpenCV format
    cv_img = np.array(img)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

    # --- Step 1: Apply Warm Tone ---
    increase_blue = np.full(cv_img.shape, (10, -5, -10), dtype=np.int16)  # BGR shift
    cv_img = np.clip(cv_img.astype(np.int16) + increase_blue, 0, 255).astype(np.uint8)

    # --- Step 2: Contrast and Brightness ---
    cv_img = cv2.convertScaleAbs(cv_img, alpha=1.1, beta=15)  # Slight brightness & contrast

    # Convert back to PIL
    img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    # --- Step 3: Enhance Vibrancy and Sharpness ---
    img = ImageEnhance.Color(img).enhance(1.35)       # More vibrant colors
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = ImageEnhance.Sharpness(img).enhance(1.3)

    # Reapply alpha if needed
    if alpha:
        img.putalpha(alpha)

    # Save with original format
    save_params = {}
    if img_format == "PNG":
        save_params["compress_level"] = 1
    elif img_format == "WEBP":
        save_params["lossless"] = True
    elif img_format in ["JPEG", "JPG"]:
        save_params["quality"] = 95

    img.save(output_path, format=img_format, **save_params)

# Batch Process
supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
for file in os.listdir(input_folder):
    if file.lower().endswith(supported_formats):
        in_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)
        apply_food_filter(in_path, out_path)
        print(f"Filtered: {file}")

print("🥕 Grocery & food images filtered with vibrant tone.")
