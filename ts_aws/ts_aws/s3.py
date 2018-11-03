import ts_config
import ts_logger

import boto3
import os

logger = ts_logger.get(__name__)

resource = boto3.resource('s3')
bucket = resource.Bucket(f"{ts_config.get('s3.buckets.media.name')}-{ts_config.get('stage')}")

def upload_file(filename, s3_key):
    logger.info("upload_file | start", s3_key=s3_key, _filename=filename)
    r = bucket.upload_file(filename, s3_key)
    logger.info("upload_file | success", r=r)

def download_file(s3_key, filename):
    logger.info("download_file | start", s3_key=s3_key, _filename=filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    r = bucket.download_file(s3_key, filename)
    logger.info("download_file | success", r=r)
