import os
import cv2
import numpy as np
from PIL import Image

input_folder = "input_images"
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

def enhance_image(image_path, output_path):
    img = Image.open(image_path)
    img_format = img.format

    if img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info):
        # Split alpha channel
        alpha = img.getchannel("A")
        img = img.convert("RGB")
    else:
        alpha = None

    # Convert to OpenCV format
    cv_img = np.array(img)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

    # Apply auto tone using histogram equalization on Y channel
    yuv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    cv_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

    # Convert back to PIL
    img_out = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    # Re-attach alpha if available
    if alpha:
        img_out.putalpha(alpha)

    # Save with proper format
    save_params = {}
    if img_format == "PNG":
        save_params["compress_level"] = 1
    elif img_format == "WEBP":
        save_params["lossless"] = True
    elif img_format in ["JPEG", "JPG"]:
        save_params["quality"] = 95

    img_out.save(output_path, format=img_format, **save_params)

# Batch process
supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
for file in os.listdir(input_folder):
    if file.lower().endswith(supported_formats):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)
        enhance_image(input_path, output_path)
        print(f"Auto-toned: {file}")

print("Batch auto-tone and color fix complete.")
