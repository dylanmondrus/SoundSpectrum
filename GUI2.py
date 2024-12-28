import os
from pathlib import Path
import ctypes
import pyautogui
import subprocess
import time

# Global variable to store the exported file name
exportedfile_name = None


def get_actual_desktop_path():
    """
    Get the actual path to the Desktop, avoiding OneDrive redirection.

    Returns:
        Path: The resolved path to the Desktop folder.
    """
    try:
        buf = ctypes.create_unicode_buffer(1024)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0000, None, 0, buf)
        return Path(buf.value)
    except Exception as e:
        print(f"Error resolving Desktop path: {e}")
        return Path.home() / "Desktop"  # Fallback to default Desktop path


def getSpectroPath():
    """
    Construct the full path to the exported spectrograph file dynamically.

    Returns:
        str: The full path to the exported spectrograph file.

    Raises:
        ValueError: If the exported file name is not set.
    """
    global exportedfile_name
    if not exportedfile_name:
        raise ValueError("The exported file name has not been set. Ensure automate_gui() runs first.")

    # Use the actual Desktop path
    desktop_path = get_actual_desktop_path()
    return os.path.join(desktop_path, f"{exportedfile_name}.txt")


def automate_gui():
    """
    Automate the GUI actions in Audacity to export the spectrograph.

    - Opens Audacity.
    - Loads the most recent audio file from the Downloads folder.
    - Automates the Analyze and Export actions.
    - Saves the exported file on the Desktop.

    Returns:
        str: The name of the exported spectrograph file.
    """
    global exportedfile_name

    try:
        # Open Audacity
        audacity_path = "C:/Program Files/Audacity/Audacity.exe"
        subprocess.Popen(audacity_path)
        print("Opening Audacity...")
        time.sleep(5)

        # Open the file dialog
        pyautogui.hotkey("ctrl", "o")
        print("Opening file dialog...")
        time.sleep(5)

        # Get the most recent file in the Downloads folder
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        files = os.listdir(downloads_path)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(downloads_path, x)), reverse=True)
        recent_file_path = os.path.join(downloads_path, files[0])

        # Open the most recent file
        pyautogui.typewrite(recent_file_path)
        pyautogui.press('enter')
        print(f"Opening file: {recent_file_path}")
        time.sleep(3)

        # Select all and analyze
        pyautogui.hotkey("ctrl", "a")
        print("Selecting all audio...")
        time.sleep(5)
        pyautogui.hotkey("ctrl", "alt", "p")
        print("Analyzing spectrum...")
        time.sleep(5)

        # Locate and click the Export button
        export_coords = pyautogui.locateOnScreen("C:/Users/dylan/Downloads/Export_screenshot_new.png", confidence=0.8)
        if not export_coords:
            raise TimeoutError("Export button not found on the screen.")
        pyautogui.click(export_coords)
        print("Exporting spectrum...")
        time.sleep(5)

        # Set the exported file name
        base_name = os.path.splitext(os.path.basename(recent_file_path))[0]
        exportedfile_name = f"{base_name}_spectrum"
        pyautogui.typewrite(exportedfile_name)
        pyautogui.press('enter')
        print(f"Exported as: {exportedfile_name}.txt")
        time.sleep(3)

        return exportedfile_name

    except Exception as e:
        print(f"Error during GUI automation: {e}")
        return None


