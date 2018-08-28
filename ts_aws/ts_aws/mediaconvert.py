import ts_config
import ts_logger

import boto3

logger = ts_logger.get(__name__)

client = boto3.client('mediaconvert', endpoint_url=ts_config.get("aws.mediaconvert.endpoint_url"))

def create_media_export(media_type, media_id):
    logger.info("create_media_export | start", media_type=media_type, media_id=media_id)
    bucket = ts_config.get('aws.s3.main.name')
    url_prefix = f"s3://{bucket}/{media_type}s/{media_id}"
    r = client.create_job(
        UserMetadata={
          'media_type': f"{media_type}",
          'media_id': f"{media_id}"
        },
        Role=ts_config.get("aws.mediaconvert.role"),
        Settings={
            'OutputGroups': [{
                  'Name': "File Group",
                  'Outputs': [{
                    'ContainerSettings': {
                        'Container': "MP4",
                        'Mp4Settings': {
                          'CslgAtom': "INCLUDE",
                          'FreeSpaceBox': "EXCLUDE",
                          'MoovPlacement': "PROGRESSIVE_DOWNLOAD"
                        }
                      },
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
                                'MaxBitrate': 10000000,
                                'SlowPal': "DISABLED",
                                'SpatialAdaptiveQuantization': "ENABLED",
                                'TemporalAdaptiveQuantization': "ENABLED",
                                'FlickerAdaptiveQuantization': "DISABLED",
                                'EntropyEncoding': "CABAC",
                                'FramerateControl': "INITIALIZE_FROM_SOURCE",
                                'RateControlMode': "QVBR",
                                'QvbrSettings': {
                                    'QvbrQualityLevel': 7
                                },
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
                                'DynamicSubGop': "STATIC"
                            }
                        },
                        'AfdSignaling': "NONE",
                        'DropFrameTimecode': "ENABLED",
                        'RespondToAfd': "NONE",
                        'ColorMetadata': "INSERT"
                    },
                    'AudioDescriptions': [{
                      'AudioTypeControl': "FOLLOW_INPUT",
                      'AudioSourceName': "Audio Selector 1",
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
                    'Extension': "mp4"
                }],
                'OutputGroupSettings': {
                    'Type': "FILE_GROUP_SETTINGS",
                    'FileGroupSettings': {
                        'Destination': f"{url_prefix}/{media_type}"
                    }
                }
            }],
            'AdAvailOffset': 0,
            'Inputs': [{
                'AudioSelectors': {
                    'Audio Selector 1': {
                        'Offset': 0,
                        'DefaultSelection': "DEFAULT",
                        'ExternalAudioFileInput': f"{url_prefix}/playlist-audio.m3u8",
                        'ProgramSelection': 1
                    }
                },
                'VideoSelector': {
                    'ColorSpace': "FOLLOW"
                },
                'FilterEnable': "AUTO",
                'PsiControl': "USE_PSI",
                'FilterStrength': 0,
                'DeblockFilter': "DISABLED",
                'DenoiseFilter': "DISABLED",
                'TimecodeSource': "EMBEDDED",
                'FileInput': f"{url_prefix}/playlist-video.m3u8"
            }]
        }
    )
    logger.info("create_media_export | success", response=r)
