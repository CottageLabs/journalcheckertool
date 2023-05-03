from setuptools import setup, find_packages

setup(
    name='jctdata',
    version='5.4.0',
    packages=find_packages(),
    install_requires=[
        "click~=8.1.3",
        "requests==2.22.0",
        "Unidecode==1.1.1",
        "Deprecated==1.2.13",
        "Markdown==3.1.1",
        "wheel",
        "PyYAML==6.0"
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
