import ts_config
import ts_logger

import boto3
import time

logger = ts_logger.get(__name__)

client = boto3.client('mediaconvert', endpoint_url=ts_config.get('mediaconvert.url'))
bucket = f"{ts_config.get('s3.buckets.media.name')}-{ts_config.get('stage')}"

def create(stream, clip, clip_segments):
    def _get_timecode(_time):
        seconds = _time // 1
        leftover = _time - seconds
        frames = str(int(stream.fps_numerator / stream.fps_denominator * leftover)).zfill(2)
        return f"{time.strftime('%H:%M:%S', time.gmtime(_time))}:{frames}"

    def _get_input_settings(clip_segment):
        settings = {
            'FilterEnable': "AUTO",
            'PsiControl': "USE_PSI",
            'FilterStrength': 0,
            'DeblockFilter': "DISABLED",
            'DenoiseFilter': "DISABLED",
            'TimecodeSource': "ZEROBASED",
            'VideoSelector': {
                'ColorSpace': "FOLLOW"
            },
            'AudioSelectors': {
                'Audio Selector 1': {
                    'Offset': 0,
                    'DefaultSelection': "DEFAULT",
                    'ProgramSelection': 1
                }
            },
            'FileInput': f"s3://{bucket}/{clip_segment.media_key}",
        }
        if clip_segment.segment_time_in is not None or clip_segment.segment_time_out is not None:
            input_clippings = {}
            if clip_segment.segment_time_in:
                input_clippings['StartTimecode'] = _get_timecode(clip_segment.segment_time_in)
            if clip_segment.segment_time_out:
                input_clippings['EndTimecode'] = _get_timecode(clip_segment.segment_time_out)
            settings['InputClippings'] = [input_clippings]
        return settings

    args = {
        'UserMetadata': {
          'clip_id': f"{clip.clip_id}",
        },
        'Queue': f"{ts_config.get('mediaconvert.queues.clip.arn-prefix')}-{ts_config.get('stage')}",
        'Role': ts_config.get('mediaconvert.role'),
        'Settings': {
            'TimecodeConfig': {
                'Source': "ZEROBASED"
            },
            'AdAvailOffset': 0,
            'Inputs': list(map(_get_input_settings, clip_segments)),
            'OutputGroups': [{
                'Name': "File Group",
                'OutputGroupSettings': {
                    'Type': "FILE_GROUP_SETTINGS",
                    'FileGroupSettings': {
                        'Destination': f"s3://{bucket}/clips/{clip.clip_id}/clip"
                    }
                },
                'Outputs': [{
                    'VideoDescription': {
                        'ScalingBehavior': "DEFAULT",
                        'TimecodeInsertion': "DISABLED",
                        'AntiAlias': "ENABLED",
                        'Sharpness': 50,
                        'CodecSettings': {
                            'Codec': "H_264",
                            'H264Settings': {
                                'InterlaceMode': "PROGRESSIVE",
                                'NumberReferenceFrames': 3,
                                'Syntax': "DEFAULT",
                                'Softness': 0,
                                'GopClosedCadence': 1,
                                'GopSize': 90,
                                'Slices': 1,
                                'GopBReference': "DISABLED",
                                'SlowPal': "DISABLED",
                                'SpatialAdaptiveQuantization': "ENABLED",
                                'TemporalAdaptiveQuantization': "ENABLED",
                                'FlickerAdaptiveQuantization': "DISABLED",
                                'EntropyEncoding': "CABAC",
                                'FramerateControl': "INITIALIZE_FROM_SOURCE",
                                'RateControlMode': "QVBR",
                                'CodecProfile': "MAIN",
                                'Telecine': "NONE",
                                'MinIInterval': 0,
                                'AdaptiveQuantization': "HIGH",
                                'CodecLevel': "AUTO",
                                'FieldEncoding': "PAFF",
                                'SceneChangeDetect': "ENABLED",
                                'QualityTuningLevel': "SINGLE_PASS",
                                'FramerateConversionAlgorithm': "DUPLICATE_DROP",
                                'UnregisteredSeiTimecode': "DISABLED",
                                'GopSizeUnits': "FRAMES",
                                'ParControl': "INITIALIZE_FROM_SOURCE",
                                'NumberBFramesBetweenReferenceFrames': 2,
                                'RepeatPps': "DISABLED",
                                'DynamicSubGop': "STATIC",
                                'QvbrSettings': {
                                    'QvbrQualityLevel': 7
                                },
                                'MaxBitrate': 10000000
                            }
                        },
                        'AfdSignaling': "NONE",
                        'DropFrameTimecode': "ENABLED",
                        'RespondToAfd': "NONE",
                        'ColorMetadata': "INSERT"
                    },
                    'AudioDescriptions': [{
                        'AudioTypeControl': "FOLLOW_INPUT",
                        'CodecSettings': {
                            'Codec': "AAC",
                            'AacSettings': {
                                'AudioDescriptionBroadcasterMix': "NORMAL",
                                'Bitrate': 96000,
                                'RateControlMode': "CBR",
                                'CodecProfile': "LC",
                                'CodingMode': "CODING_MODE_2_0",
                                'RawFormat': "NONE",
                                'SampleRate': 48000,
                                'Specification': "MPEG4"
                            }
                        },
                        'LanguageCodeControl': "FOLLOW_INPUT"
                    }],
                    'ContainerSettings': {
                        'Container': "MP4",
                        'Mp4Settings': {
                            'CslgAtom': "INCLUDE",
                            'FreeSpaceBox': "EXCLUDE",
                            'MoovPlacement': "PROGRESSIVE_DOWNLOAD"
                        }
                    },
                    'Extension': "mp4"
                }]
            }]
        }
    }

    logger.info("create_media_export | args", _args=args)
    r = client.create_job(**args)
    logger.info("create_media_export | success", response=r)
