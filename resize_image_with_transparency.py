import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

input_folder = "input_images"
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

def beautify_image(image_path, output_path):
    img = Image.open(image_path)
    img_format = img.format

    # Handle transparency
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info)
    alpha = img.getchannel("A") if has_alpha else None
    img = img.convert("RGB")

    # Convert to OpenCV format for more control
    cv_img = np.array(img)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

    # --- AUTO BRIGHTNESS & CONTRAST ---
    lab = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))
    cv_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Convert back to PIL for enhancements
    img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    # --- COLOR & SHARPNESS ENHANCEME
