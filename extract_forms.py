import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = 'http://10.0.2.7/mutillidae/index.php?page=dns-lookup.php'
response = request(target_url)

parsed_html = BeautifulSoup(response.content, features="lxml")
forms_list = parsed_html.findAll('form')

for form in forms_list:
    action = form.get('action')
    post_url = urljoin(target_url, action)
    method = form.get('method')

    inputs_list = form.findAll('input')
    post_data = {}
    for input in inputs_list:
        input_name = input.get('name')
        input_type = input.get('type')
        input_value = input.get('value')
        if input_type == 'text':
            input_value = 'test'

        post_data[input_name] = input_value

    result = requests.post(post_url, data=post_data)
    if 'Results for test' in result.content.decode('utf-8'):
        print('[+] Successfully executed')
    else:
        print('[-] Failed to execute.')
