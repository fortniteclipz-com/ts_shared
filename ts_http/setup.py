from setuptools import setup, find_packages

setup(
    name='ts_http',
    version='0.1',
    description='ts_http',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        'ts_logger==0.1',
    	'requests==2.19.1',
    ],
    dependency_links=[
        'ts_logger @ git+ssh://git@github.com/sachinahj/ts_shared.git@master#egg=ts_logger-0.1&subdirectory=ts_logger',
    ],
    zip_safe=False
)
