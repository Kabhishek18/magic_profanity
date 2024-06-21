import setuptools
from setuptools import setup, find_packages

from magic_profanity import __version__

setuptools.setup(
    name="magic_profanity",
    version=__version__,
    author="Kumar Abhishek",
    author_email="developer@kabhishek18.com",
    description='A Python library for detecting and censoring profanity in text',
    long_description=open('README.md').read(),
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
    data_files=[
        ("wordlist", ["magic_profanity/wordlist.txt"]),
        ("unicode_characters", ["magic_profanity/unicode.json"]),
    ],
    package_data={
        "better_profanity": ["wordlist.txt", "unicode.json"]
    },
    include_package_data=True,
)
