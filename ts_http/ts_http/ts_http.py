import os
import requests

def download_file(url, filename):
    r = requests.get(url)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(r.content)


