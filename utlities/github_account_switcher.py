import subprocess
import sys

github_accounts = {
    # 'username': 'useremail@email.com',
    # 'username2': 'username2@email.com'
}

# Uncomment the above part and add accounts, make sure to keep spelling correct and also the git should be configured from beforehand
if not github_accounts:
    print("\033[1;31mError: GitHub accounts not found in the file github_account_switcher.py. Please modify the file and add your GitHub accounts.\033[0m")
    sys.exit(1)

def install_inquirer():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "inquirer"], check=True)
        print("Successfully installed 'inquirer'.")
    except Exception as e:
        print(f"Error installing 'inquirer': {e}")
        sys.exit(1)

def github_account_switch(account_key):
    try:
        username = account_key
        email = github_accounts[account_key]
        subprocess.run(['git', 'config', '--global', 'user.name', username], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
        print(f"\033[1;32mSuccessfully switched to GitHub account: {username} ({email})\033[1m")
    except KeyError:
        print("\033[1;31mInvalid GitHub account key. Please choose a valid key from the dictionary.\033[0m")

def print_colored(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")

if __name__ == "__main__":
    print_colored("Available GitHub accounts:", '1')
    for key in github_accounts:
        print_colored(f"{key}: {github_accounts[key]}", "94")

    try:
        import inquirer
    except ImportError:
        print_colored("'inquirer' not found. Installing...", "1;35")
        install_inquirer()
        import inquirer

    questions = [inquirer.List('account',
                               message="Select the GitHub account you want to switch to:",
                               choices=list(github_accounts.keys()))]
    answers = inquirer.prompt(questions)

    github_account_switch(answers['account'])
