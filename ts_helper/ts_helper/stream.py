import math
import os
import subprocess

from ffprobe3 import FFProbe

def init_ff_libs():
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

def analyze_duration(media_filename):
    metadata = FFProbe(media_filename)
    for stream in metadata.streams:
        if stream.is_video() or stream.is_audio():
            return float(stream.duration)
    return 0

def calculate_gop(media_filename):
    fps = 0
    metadata = FFProbe(media_filename)
    def parse(r_frame_rate):
        [top, bottom] = r_frame_rate.split("/")
        return float(top) / float(bottom)
    for stream in metadata.streams:
        if stream.is_video() or stream.is_audio():
            fps = parse(stream.r_frame_rate)
    return math.ceil(fps / 2)

def split_media_video(media_filename, media_filename_video):
    os.makedirs(os.path.dirname(media_filename_video), exist_ok=True)
    cmd = f"ffmpeg -i {media_filename} -muxdelay 0 -an -vcodec copy -copyts -y {media_filename_video} < /dev/null"
    p = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def split_media_audio(media_filename, media_filename_audio):
    os.makedirs(os.path.dirname(media_filename_audio), exist_ok=True)
    cmd = f"ffmpeg -i {media_filename} -muxdelay 0 -vn -acodec copy -copyts -y {media_filename_audio} < /dev/null"
    p = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def fresh_media_video(gop, media_filename_raw, media_filename_fresh):
    os.makedirs(os.path.dirname(media_filename_fresh), exist_ok=True)
    cmd = f"ffmpeg -i {media_filename_raw} -muxdelay 0 -an -vcodec libx264 -profile:v main -level 3.1 -refs 1 -g {gop} -x264opts scenecut=0:bframes=0:b-pyramid=0 -copyts -y {media_filename_fresh} < /dev/null"
    p = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def probe_media_video(media_filename, packets_filename):
    os.makedirs(os.path.dirname(packets_filename), exist_ok=True)
    with open(packets_filename, 'w') as f:
        cmd = f"ffprobe -v 0 -select_streams v -show_packets -of json -i {media_filename}"
        p = subprocess.call(cmd, stdout=f, stderr=subprocess.DEVNULL, shell=True)

def probe_media_audio(media_filename, packets_filename):
    os.makedirs(os.path.dirname(packets_filename), exist_ok=True)
    with open(packets_filename, 'w') as f:
        cmd = f"ffprobe -v 0 -select_streams a -show_packets -of json -i {media_filename}"
        p = subprocess.call(cmd, stdout=f, stderr=subprocess.DEVNULL, shell=True)

def create_m3u8(segments, filename_master, filename_video, filename_audio):
    target_duration = max(segment.video_time_duration for segment in segments)
    target_duration = math.ceil(target_duration)

    os.makedirs(os.path.dirname(filename_master), exist_ok=True)
    with open(filename_master, 'w') as f:
        f.write(f"#EXTM3U\n")
        f.write(f"#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID=\"audio\",LANGUAGE=\"en\",NAME=\"English\",AUTOSELECT=YES,DEFAULT=YES,URI=\"playlist-audio.m3u8\"\n")
        f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=1,AUDIO=\"audio\"\n")
        f.write(f"playlist-video.m3u8\n")

    os.makedirs(os.path.dirname(filename_video), exist_ok=True)
    os.makedirs(os.path.dirname(filename_audio), exist_ok=True)
    with open(filename_video, 'w') as fv, open(filename_audio, 'w') as fa:
        for f in [fv, fa]:
            f.write(f"#EXTM3U\n")
            f.write(f"#EXT-X-VERSION:7\n")
            f.write(f"#EXT-X-TARGETDURATION:{target_duration}\n")
            f.write(f"#EXT-X-PLAYLIST-TYPE:VOD\n")
            f.write(f"#EXT-X-MEDIA-SEQUENCE:0\n")
            f.write(f"\n")
        for segment in segments:
            if segment.discontinuity and segment.discontinuity is not None:
                for f in [fv, fa]:
                    f.write(f"\n")
                    f.write(f"#EXT-X-DISCONTINUITY\n")
            duration_video = float('%.2f'%(segment.video_time_duration))
            duration_audio = float('%.2f'%(segment.audio_time_duration))
            fv.write(f"#EXTINF:{duration_video},\n")
            fa.write(f"#EXTINF:{duration_audio},\n")
            if segment.video_packets_byterange and segment.video_packets_byterange is not None and segment.video_packets_pos and segment.video_packets_pos is not None:
                fv.write(f"#EXT-X-BYTERANGE:{segment.video_packets_byterange}@{segment.video_packets_pos}\n")
            # if segment.audio_packets_byterange and segment.audio_packets_byterange is not None and segment.audio_packets_pos and segment.audio_packets_pos is not None:
                # fa.write(f"#EXT-X-BYTERANGE:{segment.audio_packets_byterange}@{segment.audio_packets_pos}\n")
            fv.write(f"{segment.video_url_media}\n")
            fa.write(f"{segment.audio_url_media}\n")
        for f in [fv, fa]:
            f.write(f"\n")
            f.write(f"#EXT-X-ENDLIST\n")
