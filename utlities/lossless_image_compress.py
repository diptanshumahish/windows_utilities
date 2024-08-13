#@diptanshumahish
#Image compression tool
# Keep all your images in a single folder and run the terminal and the command inside that.

import importlib
import os
import sys
import subprocess

def check_install(module_name, install_name=None):
    try:
        importlib.import_module(module_name)
    except ImportError:
        if install_name is None:
            install_name = module_name
        print(f"{module_name} not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", install_name], check=True)
            print(f"Successfully installed '{install_name}'.")
        except Exception as e:
            print(f"Error installing '{install_name}': {e}")
            sys.exit(1)

check_install("PIL", install_name="Pillow")

check_install("tqdm")
check_install("numpy")
check_install("inquirer")

from PIL import Image
import numpy as np
from tqdm import tqdm
import time
import inquirer

def get_user_confirmation():
    questions = [
        inquirer.List('start_compression', message="Do you want to start the image compression process?", choices=['Yes', 'No']),
    ]
    answers = inquirer.prompt(questions)
    return answers['start_compression'] == 'Yes'

def compress_rle(image):
    compressed_image = []
    for row in tqdm(image, desc="Analyzing", unit="px", position=0, leave=True, colour="YELLOW"):
        compressed_row = []
        current_pixel = row[0]
        count = 1
        for pixel in row[1:]:
            if np.array_equal(pixel, current_pixel):
                count += 1
            else:
                compressed_row.extend([current_pixel.tolist(), count])
                current_pixel = pixel
                count = 1
        compressed_row.extend([current_pixel.tolist(), count])
        compressed_image.append(compressed_row)
    return compressed_image

def decompress_rle(compressed_image):
    decompressed_image = []
    for row in tqdm(compressed_image, desc="Compressing", unit="px", position=0, leave=True, colour="GREEN"):
        decompressed_row = []
        for i in range(0, len(row), 2):
            pixel = row[i]
            count = row[i + 1]
            decompressed_row.extend([pixel] * count)
        decompressed_image.append(decompressed_row)
    return decompressed_image

def load_image(file_path):
    image = Image.open(file_path)
    return np.array(image)

def save_image(file_path, image_data):
    image_data = np.array(image_data, dtype=np.uint8)
    image = Image.fromarray(image_data)

    if file_path.lower().endswith('.png'):
        image.save(file_path, compress_level=9)
    else:
        image.save(file_path)

def compress_images_in_folder():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    current_directory = os.getcwd()

    compressed_folder = os.path.join(current_directory, "Compressed")
    os.makedirs(compressed_folder, exist_ok=True)

    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.HEIC']

    # Get the list of files to process
    files_to_process = [filename for filename in os.listdir(current_directory) if
                        os.path.splitext(filename.lower())[1] in image_extensions]

    total_images = len(files_to_process)
    processed_images = 0
    converted_images = 0


    progress_bar = tqdm(total=total_images, desc="Processing Images", unit="image", position=0, leave=True)

    for filename in files_to_process:
        _, file_extension = os.path.splitext(filename)
        file_extension_lower = file_extension.lower()

        # Check if the decompressed file already exists, skip if it does
        decompressed_path = os.path.join(compressed_folder, f"compressed_{filename}")
        if os.path.exists(decompressed_path):
            print(f"\033[1;92mSkipping {filename}, Compressed file already exists. 🔄\033[0m")
            processed_images += 1
            progress_bar.update(1)
            continue

        input_image_path = os.path.join(current_directory, filename)
        try:
            original_image = load_image(input_image_path)
            height, width, channels = original_image.shape
            compressed_image = compress_rle(original_image)
            compressed_path = os.path.join(compressed_folder, f"intermediate_{filename}")

            # Check if the compressed file already exists, skip if it does
            if os.path.exists(compressed_path):
                print(f"\033[1;92mSkipping {filename}, Compressed file already exists. 🔄\033[0m")
                processed_images += 1
                progress_bar.update(1)
                continue

            with open(compressed_path, "w") as file:
                for row in tqdm(compressed_image, desc=f"Writing {filename}", unit="row", position=1, leave=True,
                                colour="BLUE"):
                    file.write(",".join(map(str, row)) + "\n")

            decompressed_image = decompress_rle(compressed_image)
            save_image(decompressed_path, decompressed_image)
            os.remove(compressed_path)

            converted_images += 1
            processed_images += 1
            progress_bar.update(1)
        except Exception as e:
            print(f"\n Skipping unsupported file: {filename}. Error: {e}")
            processed_images += 1
            progress_bar.update(1)
            continue

        print(f"\nTotal Images: {total_images}, Processed Images: {processed_images}, Converted Images: {converted_images}, Remaining Images: {total_images - processed_images}")

    progress_bar.close()



def show_Head():
     print("""
\033[1;95m╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗\033[0m
\033[1;95m║ \033[0m\033[95mImage Compressor @diptanshumahish 2023 ©️ | Windows Utilities | v0.1 | 2023\033[1;95m ║\033[0m
\033[1;95m╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝\033[0m

\033[93mThe compression speed may be slower for larger images, and the processing time depends on your device.\033[0m
\033[93mPlease be patient during the conversion, and try to avoid other activities while it's in progress.\033[0m

\033[1;96mℹ️ To use the program:\033[0m
\033[1;96m1. Run the program in the folder where the image files are located.\033[0m
\033[1;96m2. A folder named "Compressed" will be created, and all compressed files will be saved there. 📁\033[0m
""")
if __name__ == "__main__":
    show_Head()
    if get_user_confirmation():
        compress_images_in_folder()
    else:
        print("🚫 Image compression process aborted.")
