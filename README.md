# BTEMAIL Login Script

BTEMAIL Login Script is a Python script that automates the process of logging into email accounts, checking for specific keywords in the inbox, and saving successful logins to a file.

## Usage

1. Populate `logins.csv`: Add email addresses and passwords to `logins.csv` file.
2. Add keywords: Add keywords you want to check for in the `keywords.txt` file.
3. Run the script: Execute the script to start checking logins.
4. Use the menu options to perform various actions such as viewing log files, modifying keywords, etc.

## Command Prompts

To run the script with default settings:
python login_script.py

arduino
Copy code

You can also specify command-line arguments to customize the behavior of the script:
python login_script.py --logins-file logins.csv --keywords-file keywords.txt --succ-logins-file succ-logins.csv --log-file login_script.log --log-level INFO

arduino
Copy code

For more information on available command-line arguments, use the `--help` option:
python login_script.py --help
