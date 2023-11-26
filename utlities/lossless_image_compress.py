import importlib
import os
import shutil
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

from PIL import Image
import numpy as np
from tqdm import tqdm
import time

def compress_rle(image):
    compressed_image = []
    for row in tqdm(image, desc="Analyzing", unit="px", position=0, leave=True,colour="YELLOW"):
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
            print("\n")
            print(f"\nSkipping {filename}, Compressed file already exists.")
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
                print("\n")
                print(f"Skipping {filename}, compressed file already exists.")
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



if __name__ == "__main__":
    compress_images_in_folder()
