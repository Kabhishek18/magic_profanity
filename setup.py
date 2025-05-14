import setuptools
from setuptools import setup, find_packages

from magic_profanity import __version__
import os
import setuptools
from setuptools import setup, find_packages

VERSION = __version__

# Get the long description from README.md
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="magic_profanity",
    version=VERSION,
    author="Kumar Abhishek",
    author_email="developer@kabhishek18.com",
    description='A Python library for detecting and censoring profanity in text',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Kabhishek18/magic_profanity",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    keywords='profanity-filter censorship text-processing',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'nltk>=3.6.0',  # For sentiment analysis
    ],
    # Include data files
    package_data={
        "magic_profanity": ["wordlist.txt", "unicode.json"]
    },
    include_package_data=True,
)