import ts_config
import ts_logger

import boto3
import time

logger = ts_logger.get(__name__)

client = boto3.client('mediaconvert', endpoint_url=ts_config.get('mediaconvert.url'))
bucket = f"{ts_config.get('s3.buckets.media.name')}"

def create(montage, clips):
    def _get_input_settings(clip):
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
            'FileInput': f"s3://{bucket}/{clip.media_key}",
        }
        return settings

    args = {
        'UserMetadata': {
          'montage_id': f"{montage.montage_id}",
        },
        'Queue': f"{ts_config.get('mediaconvert.queues.montage.arn')}",
        'Role': ts_config.get('mediaconvert.role'),
        'Settings': {
            'TimecodeConfig': {
                'Source': "ZEROBASED"
            },
            'AdAvailOffset': 0,
            'Inputs': list(map(_get_input_settings, clips)),
            'OutputGroups': [{
                'Name': "File Group",
                'OutputGroupSettings': {
                    'Type': "FILE_GROUP_SETTINGS",
                    'FileGroupSettings': {
                        'Destination': f"s3://{bucket}/montages/{montage.montage_id}/montage"
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
