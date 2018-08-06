from setuptools import setup, find_packages

setup(
    name='ts_helper',
    version='0.1',
    description='ts_helper',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        "ts_config==0.1",
        "ts_logger==0.1",
        "requests",
        "boto3",
        "ffprobe3==0.1.2",
        "shortuuid==0.5.0",
    ],
    zip_safe=False
)
