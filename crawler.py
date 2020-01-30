import requests


url = 'mailx.ssssgoogle.com'
try:
    get_response = requests.get('http://' + url)
    print(get_response)
except requests.exceptions.ConnectionError:
    pass
