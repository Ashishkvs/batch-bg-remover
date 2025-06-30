import os
import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, StringVar, OptionMenu
from PIL import Image, ImageEnhance, ImageTk
from rembg import remove
from io import BytesIO

# Output folder
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

# Resize config
max_width = 800
max_height = 800

# Filters
FILTERS = ["Warm Boost", "Vibrant Pop", "Neutral Clean"]

def remove_background(img_path):
    with open(img_path, "rb") as f:
        result = remove(f.read())
    return Image.open(BytesIO(result)).convert("RGBA")

def resize_image(img):
    img.thumbnail((max_width, max_height), Image.LANCZOS)
    return img

def apply_filter(img, filter_type):
    rgb = img.convert("RGB")
    cv_img = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)

    # Filter logic
    if filter_type == "Warm Boost":
        tone = np.full(cv_img.shape, (10, -3, -10), dtype=np.int16)
    elif filter_type == "Vibrant Pop":
        tone = np.full(cv_img.shape, (5, 5, 5), dtype=np.int16)
    elif filter_type == "Neutral Clean":
        tone = np.full(cv_img.shape, (0, 0, 0), dtype=np.int16)
    else:
        tone = np.zeros_like(cv_img)

    cv_img = np.clip(cv_img.astype(np.int16) + tone, 0, 255).astype(np.uint8)
    rgb = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    # Enhancements
    if filter_type == "Warm Boost":
        rgb = ImageEnhance.Color(rgb).enhance(1.2)
        rgb = ImageEnhance.Contrast(rgb).enhance(1.1)
    elif filter_type == "Vibrant Pop":
        rgb = ImageEnhance.Color(rgb).enhance(1.5)
        rgb = ImageEnhance.Contrast(rgb).enhance(1.15)
    elif filter_type == "Neutral Clean":
        rgb = ImageEnhance.Color(rgb).enhance(1.05)
        rgb = ImageEnhance.Contrast(rgb).enhance(1.0)

    # Restore alpha
    alpha = img.getchannel("A")
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out

def process_images(filter_name):
    file_paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
    if not file_paths:
        return

    for file_path in file_paths:
        try:
            img = remove_background(file_path)
            img = resize_image(img)
            img = apply_filter(img, filter_name)

            base_name = os.path.basename(file_path)
            output_path = os.path.join(output_folder, base_name)
            ext = os.path.splitext(base_name)[-1].lower()

            params = {"quality": 95} if ext in [".jpg", ".jpeg"] else {}
            img.save(output_path, **params)
            print(f"✅ Processed: {base_name}")
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

    print("🎯 All selected images processed.")

# GUI setup
root = Tk()
root.title("Grocery Image Filter Tool")
root.geometry("400x200")

label = Label(root, text="Select Filter:", font=("Arial", 12))
label.pack(pady=10)

selected_filter = StringVar(root)
selected_filter.set(FILTERS[0])
filter_menu = OptionMenu(root, selected_filter, *FILTERS)
filter_menu.pack()

btn = Button(root, text="Select Images and Apply Filter", font=("Arial", 11), command=lambda: process_images(selected_filter.get()))
btn.pack(pady=20)

output_note = Label(root, text="Output saved in 'output_images/'", fg="green")
output_note.pack()

root.mainloop()
