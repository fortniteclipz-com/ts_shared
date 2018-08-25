from setuptools import setup, find_packages

setup(
    name='ts_media',
    version='0.1',
    description='ts_media',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        "ts_logger==0.1",
        "ffprobe3==0.1.2",
    ],
    dependency_links=[
        "git+ssh://git@github.com/sachinahj/ts_shared.git@master#egg=ts_logger-0.1&subdirectory=ts_logger",
    ],
    zip_safe=False
)
