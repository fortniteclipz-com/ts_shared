from setuptools import setup, find_packages

setup(
    name='ts_stream',
    version='0.1',
    description='ts_stream',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        "ffprobe3==0.1.2",
    ],
    zip_safe=False
)
