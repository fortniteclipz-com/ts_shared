import ts_logger

import json
import os

logger = ts_logger.get(__name__)

def save_json(data, json_filename):
    logger.info("save_json | start", data=data, json_filename=json_filename)
    os.makedirs(os.path.dirname(json_filename), exist_ok=True)
    with open(json_filename, 'w') as f:
        json.dump(data, f)
    logger.info("save_json | success")

def get_json(filename):
    logger.info("get_json | start", filename_=filename)
    with open(filename, 'r') as f:
        data =  json.load(f)
        logger.info("get_json | success", data=data)
        return

def delete(filename):
    logger.info("delete | start", filename_=filename)
    os.remove(filename)
    logger.info("delete | success")
