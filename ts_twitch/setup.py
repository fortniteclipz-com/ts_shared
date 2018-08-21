from setuptools import setup, find_packages

setup(
    name='ts_twitch',
    version='0.1',
    description='ts_twitch',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        "streamlink==0.14.2",
    ],
    zip_safe=False
)
