from setuptools import setup, find_packages

setup(
    name='jct',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        "elasticsearch==7.13.0",
        "flask",
        "Flask-Cors",
        "numpy<2",    # Elasticsearch==7.13.0 requires numpy<2, and we can't upgrade our ES library while we are on OSS
        "requests~=2.32.3",
        "Werkzeug"
        # "click~=8.1.3",
        # "requests==2.22.0",
        # "Unidecode==1.1.1",
        # "Deprecated==1.2.13",
        # "Markdown==3.1.1",
        # "wheel",
        # "PyYAML==6.0.1"
    ],
    url='http://journalcheckertool.org/',
    author='Cottage Labs',
    author_email='us@cottagelabs.com',
    description='Journal Checker Tool algorithm and API',
    license='Apache 2.0',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
