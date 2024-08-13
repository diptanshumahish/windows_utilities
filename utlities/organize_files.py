# Organize files
import os
import shutil
import sys
from tqdm import tqdm
from colorama import Fore, Style, init
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


try:
    from colorama import Fore, Style, init
except ImportError:
    print("Colorama not found. Installing...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
        print("Successfully installed 'colorama'.")
    except Exception as e:
        print(f"Error installing 'colorama': {e}")
        sys.exit(1)

from tqdm import tqdm
import time

def organize_files(source_folder):

    files = os.listdir(source_folder)
    file_type_folders = {}

    for file in tqdm(files, desc="Organizing Files", unit="file", dynamic_ncols=True):
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file)
            file_type = get_file_type(file_extension)
            
            if file_type:
                if file_type not in file_type_folders:
                    file_type_folders[file_type] = os.path.join(source_folder, f'{file_type.capitalize()}')
                    os.makedirs(file_type_folders[file_type], exist_ok=True)
                shutil.move(file_path, os.path.join(file_type_folders[file_type], file))

    print(f"\n{Fore.GREEN}{Style.BRIGHT}Files organized successfully!{Style.RESET_ALL}")
    print(f"Organized files into {len(file_type_folders)} folders:")
    for file_type, folder_path in file_type_folders.items():
        print(f" - {file_type.capitalize()}: {folder_path}")

def get_file_type(file_extension):
    file_types = {
    '.jpg': 'images',
    '.jpeg': 'images',
    '.png': 'images',
    '.gif': 'images',
    '.heic': 'images',
    '.mov': 'videos',
    '.mp4': 'videos',
    '.avi': 'videos',
    '.pdf': 'documents',
    '.doc': 'documents',
    '.docx': 'word',
    '.exe': 'apps',
    '.zip': 'compressed',
    '.rar': 'compressed',
    '.7zip': 'compressed',
    '.mp3': 'music',
    '.wav': 'music',
    '.apk': 'APK files',
    '.ttf': 'fonts',
    '.xlsx': 'excel',
    '.pptx': 'powerpoint',
    '.txt': 'text',
    '.html': 'web',
    '.css': 'stylesheets',
    '.js': 'javascript',
    '.py': 'python',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.h': 'header',
    '.json': 'json',
    '.xml': 'xml',
    '.sql': 'sql',
    '.php': 'php',
    '.asp': 'asp',
    '.jsp': 'jsp',
    '.bat': 'batch',
    '.sh': 'shell',
    '.md': 'markdown',
    '.log': 'logs',
    '.dll': 'dll',
    '.ico': 'icons',
    '.psd': 'photoshop',
    '.ai': 'illustrator',
    '.svg': 'svg',
    '.fla': 'flash',
    '.mpg': 'mpeg',
    '.wmv': 'windows_media',
    '.flv': 'flash_video',
    '.aac': 'aac',
    '.ogg': 'ogg',
    '.flac': 'flac',
    '.mpg': 'mpeg',
    '.mpeg': 'mpeg',
    '.m4a': 'm4a',
    '.m4v': 'm4v',
    '.3gp': '3gp',
    '.jar': 'java_archive',
    '.war': 'web_archive',
    '.ear': 'enterprise_archive',
    '.class': 'java_class',
    '.jsp': 'java_server_page',
    '.pyc': 'python_compiled',
    '.bak': 'backup',
    '.tmp': 'temp',
    '.swf': 'flash_movie',
    '.cfg': 'config',
    '.ini': 'ini',
    '.yml': 'yaml',
    '.bat': 'batch',
    '.dll': 'dll',
    '.jar': 'java_archive',
    '.war': 'web_archive',
    '.ear': 'enterprise_archive',
    '.class': 'java_class',
    '.apk': 'android_package',
    '.deb': 'debian_package',
    '.rpm': 'rpm_package',
    '.img': 'disk_image',
    '.iso': 'iso_image',
    '.csv': 'csv',
    '.xls': 'excel',
    '.xlsm': 'excel_macro',
    '.ppt': 'powerpoint',
    '.pptx': 'powerpoint',
    '.key': 'keynote',
    '.ods': 'open_document_spreadsheet',
    '.odt': 'open_document_text',
    '.odp': 'open_document_presentation',
    '.ogg': 'ogg',
    '.ogv': 'ogg_video',
    '.ogm': 'ogg_media',
    '.ogx': 'ogg',
    '.ogx': 'ogg',
    '.ico': 'icon',
    '.icns': 'iconset',
    '.dmg': 'disk_image',
    '.app': 'macos_app',
    '.bat': 'batch',
    '.cmd': 'windows_batch',
    '.sh': 'shell',
    '.bash': 'bash_script',
    '.ps1': 'powershell',
    '.psm1': 'powershell_module',
    '.bat': 'batch',
    '.cmd': 'windows_batch',
    '.sh': 'shell',
    '.bash': 'bash_script',
    '.ps1': 'powershell',
    '.psm1': 'powershell_module',
    '.bat': 'batch',
    '.cmd': 'windows_batch',
    '.sh': 'shell',
    '.bash': 'bash_script',
    '.ps1': 'powershell',
    '.psm1': 'powershell_module',
}
    return file_types.get(file_extension.lower(), 'other')

if __name__ == "__main__":
    source_folder = os.getcwd()
    organize_files(source_folder)
