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
            'ts_config_dev.yml',
            'ts_config_prod.yml',
        ]
    },
    install_requires=[
        'PyYAML==3.13',
    ],
    dependency_links=[],
    zip_safe=False
)
