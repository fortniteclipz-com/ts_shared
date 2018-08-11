from setuptools import setup, find_packages

setup(
    name='ts_aws',
    version='0.1',
    description='ts_aws',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        "ts_config==0.1",
        "boto3==1.7.75",
        "ffprobe3==0.1.2",
        "shortuuid==0.5.0",
    ],
    zip_safe=False
)
