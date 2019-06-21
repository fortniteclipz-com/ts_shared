import boto3
import botocore
import os

import ts_logger

logger = ts_logger.get(__name__)

logger.info("ts_aws | boto", boto3_version=boto3.__version__, botocore_version=botocore.__version__)
logger.info("ts_aws | environment", environ=os.environ, optdir=os.listdir("/opt"))
