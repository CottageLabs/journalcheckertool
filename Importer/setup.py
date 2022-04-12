from setuptools import setup, find_packages

setup(
    name='jctdata',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "requests==2.22.0",
        "Unidecode==1.1.1"
    ],
    url='http://journalcheckertool.org/',
    author='Cottage Labs',
    author_email='us@cottagelabs.com',
    description='Journal Checker Tool data importers',
    license='Apache 2.0',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
