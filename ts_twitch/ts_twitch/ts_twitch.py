import ts_aws.dynamodb.stream
import ts_file
import ts_http
import ts_media

import re
import streamlink

def initialize_stream(stream_id):
    # get raw m3u8 url from twitch stream url
    twitch_stream_url = f"http://twitch.tv/videos/{stream_id}"
    twitch_streams = streamlink.streams(twitch_stream_url)
    if 'best' not in twitch_streams:
        return (None, None)
    twitch_stream = twitch_streams['best']
    twitch_stream_url_prefix = "/".join(twitch_stream.url.split("/")[:-1])

    # download raw m3u8 and extract segment info from m3u8
    playlist_filename = f"/tmp/playlist-raw.m3u8"
    ts_http.download_file(twitch_stream.url, playlist_filename)
    stream_segments = []
    ss = ts_aws.dynamodb.stream.StreamSegment()
    with open(playlist_filename, 'r') as f:
        for line in f:
            if "EXTINF" in line:
                time_duration_raw = line.strip()
                time_duration = float(re.findall("\d+\.\d+", time_duration_raw)[0])
                ss.time_duration = time_duration
            if ".ts" in line:
                segment_raw = line.strip()
                segment = int(''.join(filter(str.isdigit, segment_raw)))
                segment_padded = str(segment).zfill(6)
                url_media_raw = f"{twitch_stream_url_prefix}/{segment_raw}"
                ss.segment = segment
                ss.padded = segment_padded
                ss.url_media_raw = url_media_raw
            if ss.time_duration is not None and ss.segment is not None:
                stream_segments.append(ss)
                ss = ts_aws.dynamodb.stream.StreamSegment()

    # download first segment, probe, and get stream_time_offset
    first_ss = stream_segments[0]
    media_filename = f"/tmp/{first_ss.padded}.ts"
    packets_filename = f"/tmp/{first_ss.padded}.json"
    ts_http.download_file(first_ss.url_media_raw, media_filename)
    ts_media.probe_media_video(media_filename, packets_filename)
    packets_video = ts_file.get_json(packets_filename)['packets']
    stream_time_offset = float(packets_video[0]['pts_time'])

    # delete tmp files
    ts_file.delete(playlist_filename)
    ts_file.delete(media_filename)
    ts_file.delete(packets_filename)

    # add stream_id, time_in, and time_out to stream_segments
    timestamp = stream_time_offset
    for ss in stream_segments:
        ss.stream_id = stream_id
        ss.time_in = timestamp
        timestamp += ss.time_duration
        ss.time_out = timestamp

    # gather stream_data
    stream = ts_aws.dynamodb.stream.Stream(
        stream_id=stream_id,
        time_offset=stream_time_offset,
        url_playlist_raw=twitch_stream.url,
    )

    return (stream, stream_segments)
