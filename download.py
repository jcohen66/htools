import requests
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(get_response.content)
    os.remove(file_name)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
url = 'https://image.freepik.com/free-photo/attractive-woman-speaking-smartphone_23-2147848964.jpg'
download(url)
