from setuptools import setup, find_packages

setup(
    name="rowservice",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'Flask>=3.1.0',
        'Flask-Cors>=5.0.0',
        'Flask-PyMongo>=2.3.0',
        'python-dotenv>=1.0.1',
        'pymongo>=4.10.1',
    ],
)
