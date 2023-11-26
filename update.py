import os
import shutil
import subprocess

# Check if colorama is installed, and install it if necessary
try:
    from colorama import init, Fore, Style
except ImportError:
    print("Installing colorama...")
    subprocess.run(["pip", "install", "colorama"])

# Check if tqdm is installed, and install it if necessary
try:
    import tqdm
except ImportError:
    print("Installing tqdm...")
    subprocess.run(["pip", "install", "tqdm"])

# Initialize colorama for colored output

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip(), error.decode().strip()

def update_repository():
    print(f"{Fore.CYAN}Updating the repository...{Style.RESET_ALL}")
    output, error = run_command("git pull")
    if error:
        print(f"{Fore.RED}Error updating the repository:{Style.RESET_ALL}\n{error}")
        exit(1)

def copy_files():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_dir = os.path.join(script_dir, 'utilities')
    destination_dir = script_dir

    print(f"{Fore.GREEN}Copying new files...{Style.RESET_ALL}")
    for root, _, files in os.walk(source_dir):
        for file in tqdm.tqdm(files, unit='file', desc="Copying"):
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.copy2(source_path, destination_path)

def main():
    # Update repository
    update_repository()

    # Copy new files
    copy_files()

    print(f"\n{Fore.GREEN}Update complete! {Fore.WHITE}Thank you for using this tool!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
