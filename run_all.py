import subprocess
import shutil
import os

def move_images(src_folder, dst_folder):
    # Check if source folder exists
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)
    
    # Move all files from src_folder to dst_folder
    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        dst_path = os.path.join(dst_folder, filename)
        try:
            shutil.move(src_path, dst_path)
            print(f"Moved {filename} to {dst_folder}")
        except Exception as e:
            print(f"Error moving {filename}: {e}")

# Define the folders
input_images_folder = 'input_images'
output_images_folder = 'output_images'

# Run resize_bg.py
print("Running resize_bg.py...")
subprocess.run(["python", "resize_bg.py"])

# Move images from output_images to input_images
print("Moving images from output_images to input_images...")
move_images(output_images_folder, input_images_folder)

# Run remove_bg.py
print("Running remove_bg.py...")
subprocess.run(["python", "remove_bg.py"])

# Move images again
print("Moving images from output_images to input_images...")
move_images(output_images_folder, input_images_folder)

# Run food_grocery_filter.py
print("Running food_grocery_filter.py...")
subprocess.run(["python", "food_grocery_filter.py"])

# Final move (if needed)
print("Moving images from output_images to input_images...")
# move_images(output_images_folder, input_images_folder)

print("All scripts executed and images transferred.")
