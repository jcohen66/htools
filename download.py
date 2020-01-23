import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(get_response.content)

download('https://image.freepik.com/free-photo/attractive-woman-speaking-smartphone_23-2147848964.jpg')