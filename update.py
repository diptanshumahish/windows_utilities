import os
import shutil
import subprocess
from tqdm import tqdm as tqdm_progress
from colorama import init, Fore, Style

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
init()

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip(), error.decode().strip()

def update_repository():
    print(f"{Fore.CYAN}Updating the repository...{Style.RESET_ALL}")
    output, error = run_command("git pull")
    if error:
        print(f"{Fore.RED}Error updating the repository:{Style.RESET_ALL}\n{error}")
        print(f"{Fore.BLUE}You can retry this command.{Style.RESET_ALL}")
        exit(1)

def copy_files():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_dir = os.path.join(script_dir, 'utilities')
    destination_dir = script_dir

    print(f"{Fore.BLUE}Copying new files...{Style.RESET_ALL}")
    added_files = []

    with tqdm_progress(unit='file', desc="Copying") as pbar:
        for root, _, files in os.walk(source_dir):
            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)

                print(f"Source: {source_path}, Destination: {destination_path}")

                if not os.path.exists(destination_path):
                    added_files.append(file)
                    shutil.copy2(source_path, destination_path)

                pbar.update(1)

    print(f"\n{Fore.GREEN}Copy complete!{Style.RESET_ALL}")

    if added_files:
        print(f"{Fore.YELLOW}Added files:{Style.RESET_ALL}")
        for file in added_files:
            print(f"{Fore.YELLOW}- {file}{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}No new files added.{Style.RESET_ALL}")

def main():
    update_repository()
    copy_files()

    print(f"\n{Fore.GREEN}Update complete! \n{Fore.WHITE}Thank you for using the Windows Utilities Tools (●'◡'●){Style.RESET_ALL}")

if __name__ == "__main__":
    main()
