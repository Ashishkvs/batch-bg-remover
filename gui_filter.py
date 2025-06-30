import os
import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, StringVar, OptionMenu, Canvas, PhotoImage, Toplevel
from PIL import Image, ImageEnhance, ImageTk
from rembg import remove
from io import BytesIO

# Config
output_folder = "output_images"
max_width = 800
max_height = 800
os.makedirs(output_folder, exist_ok=True)

FILTERS = ["Warm Boost", "Vibrant Pop", "Neutral Clean"]
selected_filter = None
preview_image = None

def remove_background(image_path):
    with open(image_path, "rb") as f:
        result = remove(f.read())
    return Image.open(BytesIO(result)).convert("RGBA")

def resize_image(img):
    img.thumbnail((max_width, max_height), Image.LANCZOS)
    return img

def apply_filter(img, filter_type):
    rgb = img.convert("RGB")
    cv_img = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)

    # Apply tone
    if filter_type == "Warm Boost":
        tone = np.full(cv_img.shape, (10, -3, -10), dtype=np.int16)
    elif filter_type == "Vibrant Pop":
        tone = np.full(cv_img.shape, (5, 5, 5), dtype=np.int16)
    elif filter_type == "Neutral Clean":
        tone = np.zeros_like(cv_img, dtype=np.int16)
    else:
        tone = np.zeros_like(cv_img, dtype=np.int16)

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

    # Restore alpha
    alpha = img.getchannel("A")
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out

def show_preview():
    global preview_image
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
    if not file_path:
        return

    try:
        img = remove_background(file_path)
        img = resize_image(img)
        filtered = apply_filter(img, selected_filter.get())

        # Create preview window
        top = Toplevel()
        top.title("Live Filter Preview")

        preview_image = ImageTk.PhotoImage(filtered.resize((300, 300)))
        canvas = Canvas(top, width=300, height=300)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=preview_image)
        Label(top, text="Preview with filter: " + selected_filter.get()).pack()

    except Exception as e:
        print(f"❌ Error showing preview: {e}")

def process_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
    if not file_paths:
        return

    for file_path in file_paths:
        try:
            img = remove_background(file_path)
            img = resize_image(img)
            img = apply_filter(img, selected_filter.get())

            base = os.path.basename(file_path)
            out_path = os.path.join(output_folder, base)
            ext = os.path.splitext(base)[-1].lower()

            params = {"quality": 95} if ext in [".jpg", ".jpeg"] else {}
            img.save(out_path, **params)
            print(f"✅ Processed: {base}")
        except Exception as e:
            print(f"❌ Error: {file_path}: {e}")

    print("🎯 All images processed and saved.")

# GUI Setup
root = Tk()
root.title("🛒 Grocery Image Filter Tool")
root.geometry("400x280")

Label(root, text="Select Filter:", font=("Arial", 12)).pack(pady=10)

selected_filter = StringVar(root)
selected_filter.set(FILTERS[0])
OptionMenu(root, selected_filter, *FILTERS).pack()

Button(root, text="👁 Preview Filter on Image", font=("Arial", 10), command=show_preview).pack(pady=10)
Button(root, text="📂 Select Images & Apply Filter", font=("Arial", 10), command=process_images).pack(pady=10)

Label(root, text="Processed images will be saved in:\n'output_images/' folder", fg="green").pack(pady=20)

root.mainloop()
