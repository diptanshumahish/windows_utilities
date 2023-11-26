@echo off
setlocal

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Pull the latest changes from the remote repository
cd /d "%SCRIPT_DIR%"
git pull

REM Check if tqdm is installed, and install it if necessary
python -m pip show tqdm 2>nul || python -m pip install tqdm

REM Run Python script for a better user experience
python - <<EOF
import os
import shutil
try:
    from tqdm import tqdm
except ImportError:
    print("Error: tqdm is not installed. Please install it using 'pip install tqdm'")
    exit(1)

# Get the script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Copy new files to the current folder
source_dir = os.path.join(script_dir, 'utilities')
destination_dir = script_dir

print("Copying new files:")
for root, _, files in os.walk(source_dir):
    for file in tqdm(files, unit='file'):
        source_path = os.path.join(root, file)
        destination_path = os.path.join(destination_dir, file)
        shutil.copy2(source_path, destination_path)

print("Update complete!")
EOF
