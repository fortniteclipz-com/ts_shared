from setuptools import setup, find_packages

setup(
    name='ts_aws',
    version='0.1',
    description='ts_aws',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        'ts_config',
        'ts_logger',
        'ts_model',
        'boto3==1.7.75',
        'botocore==1.10.84',
        "PyMySQL==0.9.2",
        "SQLAlchemy==1.2.10",
    ],
    dependency_links=[
        'git+ssh://git@github.com/fortniteclipz/ts_shared.git@master#egg=ts_config-0.1&subdirectory=ts_config',
        'git+ssh://git@github.com/fortniteclipz/ts_shared.git@master#egg=ts_logger-0.1&subdirectory=ts_logger',
        'git+ssh://git@github.com/fortniteclipz/ts_shared.git@master#egg=ts_model-0.1&subdirectory=ts_model',
    ],
    zip_safe=False
)
