from setuptools import setup, find_packages

setup(
    name='ts_config',
    version='0.1',
    description='ts_config',
    author='Ahuja',
    license='',
    packages=find_packages(),
    package_data={
        'ts_config': [
            'ts_config.yml',
        ]
    },
    install_requires=[
        'PyYAML',
    ],
    zip_safe=False
)
