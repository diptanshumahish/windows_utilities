import inquirer
import subprocess
import sys

def install_package(package):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
        print(f"Successfully installed '{package}'.")
    except Exception as e:
        print(f"Error installing '{package}': {e}")
        sys.exit(1)

# Check if 'inquirer' is installed, and install if not
try:
    import inquirer
except ImportError:
    print("Inquirer not found. Installing...")
    install_package("inquirer")

import inquirer

def screen_sleep(choice):
    if choice == 1:
        subprocess.run(['powercfg', '/change', 'standby-timeout-ac', '5'], check=True)
        subprocess.run(['powercfg', '/change', 'standby-timeout-dc', '5'], check=True)
        print("Screen sleep time set to 5 minutes.")
    elif choice == 2:
        subprocess.run(['powercfg', '/change', 'standby-timeout-ac', '0'], check=True)
        subprocess.run(['powercfg', '/change', 'standby-timeout-dc', '0'], check=True)
        print("Screen sleep time set to never.")
    elif choice == 3:
        print("Exiting...")
        sys.exit()
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")

def main():
    questions = [
        inquirer.List('choice',
                      message="Select an option:",
                      choices=[
                          'Set screen sleep time to 5 minutes',
                          'Set screen sleep time to never',
                          'Exit'
                      ]),
    ]

    answers = inquirer.prompt(questions)

    if answers['choice'] == 'Set screen sleep time to 5 minutes':
        screen_sleep(1)
    elif answers['choice'] == 'Set screen sleep time to never':
        screen_sleep(2)
    elif answers['choice'] == 'Exit':
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
