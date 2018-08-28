import ts_config
import ts_logger

import boto3
import json
import os

logger = ts_logger.get(__name__)

resource = boto3.resource('s3')
bucket_main = resource.Bucket(ts_config.get('aws.s3.main.name'))
bucket_thumbnails = resource.Bucket(ts_config.get('aws.s3.thumbnails.name'))

def upload_file(filename, s3_key):
    logger.info("upload_file | start", s3_key=s3_key, _filename=filename)
    r = bucket_main.upload_file(filename, s3_key)
    logger.info("upload_file | success", r=r)

def download_file(s3_key, filename):
    logger.info("download_file | start", s3_key=s3_key, _filename=filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    r = bucket_main.download_file(s3_key, filename)
    logger.info("download_file | success", r=r)

