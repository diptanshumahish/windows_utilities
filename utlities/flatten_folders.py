import os
import shutil
import sys
import subprocess

try:
    from tqdm import tqdm
except ImportError:
    print("TQDM not found. Installing...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "tqdm"], check=True)
        print("Successfully installed 'tqdm'.")
    except Exception as e:
        print(f"Error installing 'tqdm': {e}")
        sys.exit(1)

from tqdm import tqdm
import time

def flatten_folders(current_folder):
    all_files = [os.path.join(root, file) for root, dirs, files in os.walk(current_folder) for file in files]

    total_files = len(all_files)
    processed_files = 0

    with tqdm(total=total_files, desc="Flattening Folders", unit="file") as progress_bar:
        for file_path in all_files:
            dest_path = os.path.join(current_folder, os.path.basename(file_path))
            if os.path.exists(dest_path):
                os.remove(file_path)
            else:
                shutil.move(file_path, dest_path)

            processed_files += 1
            progress_bar.update(1)
            time.sleep(0.1)

    for root, dirs, files in os.walk(current_folder, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            try:
                os.rmdir(folder_path)
            except OSError:
                pass

    print(f"\nFlattening completed! Processed {processed_files}/{total_files} files.")
    print(f"Subfolders have been removed.")

if __name__ == "__main__":
    current_folder = os.getcwd()
    flatten_folders(current_folder)
