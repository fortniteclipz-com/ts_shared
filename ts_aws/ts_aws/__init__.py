import boto3
import botocore

import ts_logger

logger = ts_logger.get(__name__)

logger.info("boto3 version", boto3_version=boto3.__version__)
logger.info("botocore version", botocore_version=botocore.__version__)
