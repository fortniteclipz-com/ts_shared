import ts_logger

import os
import requests

logger = ts_logger.get(__name__)

def download_file(url, filename):
    logger.info("download_file | start", url=url, filename=filename)
    r = requests.get(url)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(r.content)


