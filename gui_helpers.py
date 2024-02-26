# gui_helpers.py

import tkinter as tk
from tkinter import filedialog

def pick_file(title, filetypes):
    """
    Opens a file dialog to pick a file.
    Returns the selected file path.
    """
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def pick_directory(title):
    """
    Opens a directory dialog to pick a directory.
    Returns the selected directory path.
    """
    directory_path = filedialog.askdirectory(title=title)
    return directory_path
