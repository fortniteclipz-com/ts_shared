import ts_logger

import os
import subprocess

logger = ts_logger.get(__name__)

def init_ff_libs():
    logger.info("init_ff_libs | start")
    if 'LAMBDA_TASK_ROOT' in os.environ:
        os.environ['PATH'] = f"{os.environ['PATH']}:/tmp/"
        cmds = [
            "mv /var/task/libs/ffprobe /tmp/",
            "mv /var/task/libs/ffmpeg /tmp/",
            "chmod 755 /tmp/ffprobe",
            "chmod 755 /tmp/ffmpeg",
        ]
        for cmd in cmds:
            p = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    logger.info("init_ff_libs | success")

def thumbnail_media_video(media_filename, thumbnail_filename_pattern):
    logger.info("thumbnail_media_video | start", media_filename=media_filename, thumbnail_filename_pattern=thumbnail_filename_pattern)
    os.makedirs(os.path.dirname(thumbnail_filename_pattern), exist_ok=True)
    cmd = f"ffmpeg -i {media_filename} -vf fps=2 -q:v 1 {thumbnail_filename_pattern}"
    p = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    logger.info("thumbnail_media_video | success")
