import ts_config
import ts_logger

import boto3
import time

logger = ts_logger.get(__name__)

client = boto3.client('mediaconvert', endpoint_url=ts_config.get('aws.mediaconvert.url'))
bucket = ts_config.get('aws.s3.main.name')

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

    if clip_segment.time_in is not None or clip_segment.time_out is not None:
        input_clippings = {}
        if clip_segment.time_in:
            input_clippings['StartTimecode'] = f"{time.strftime('%H:%M:%S', time.gmtime(clip_segment.time_in))}:00"
        if clip_segment.time_out:
            input_clippings['EndTimecode'] = f"{time.strftime('%H:%M:%S', time.gmtime(clip_segment.time_out))}:00"
        settings['InputClippings'] = [input_clippings]

    return settings

def create(clip, clip_segments):
    args = {
        'UserMetadata': {
          'clip_id': f"{clip.clip_id}",
        },
        'Queue': ts_config.get('aws.mediaconvert.clip'),
        'Role': ts_config.get('aws.mediaconvert.role'),
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
            }],

        }
    }

    logger.info("create_media_export | args", _args=args)
    r = client.create_job(**args)
    logger.info("create_media_export | success", response=r)
