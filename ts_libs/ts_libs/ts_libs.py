import ts_logger

import os
import subprocess

logger = ts_logger.get(__name__)

def init():
    logger.info("init | start")
    # if 'LAMBDA_TASK_ROOT' in os.environ:
    #     os.environ['PATH'] = f"{os.environ['PATH']}:/tmp/"
    #     os.environ['LD_LIBRARY_PATH'] = "/tmp/lib"
    #     os.environ['TESSDATA_PREFIX'] = "/tmp/tessdata"
    #     cmds = [
    #         "mv /var/task/libs/ffprobe /tmp/",
    #         "chmod 755 /tmp/ffprobe",

    #         "mv /var/task/libs/ffmpeg /tmp/",
    #         "chmod 755 /tmp/ffmpeg",

    #         "mv /var/task/libs/tesseract/lib /tmp/",
    #         "mv /var/task/libs/tesseract/tessdata /tmp/",
    #         "mv /var/task/libs/tesseract/tesseract /tmp/",
    #         "chmod 755 /tmp/tesseract",
    #     ]
    #     for cmd in cmds:
    #         p = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

    logger.info("init | info", environ=os.environ, path=os.environ['PATH'], tmpdir=os.listdir("/tmp"), optdir=os.listdir("/opt"))
    logger.info("init | success")
