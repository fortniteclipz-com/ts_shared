from setuptools import setup, find_packages

setup(
    name='ts_logger',
    version='0.1',
    description='ts_logger',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
        'ts_config==0.1',
        'daiquiri==1.5.0',
        # 'python-json-logger==0.1.9',
    ],
    dependency_links=[
        'ts_config @ git+ssh://git@github.com/sachinahj/ts_shared.git@master#egg=ts_config-0.1&subdirectory=ts_config',
    ],
    zip_safe=False
)
