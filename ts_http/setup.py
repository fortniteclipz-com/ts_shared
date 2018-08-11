from setuptools import setup, find_packages

setup(
    name='ts_http',
    version='0.1',
    description='ts_http',
    author='Ahuja',
    license='',
    packages=find_packages(),
    install_requires=[
    	"requests==2.19.1"
    ],
    zip_safe=False
)
