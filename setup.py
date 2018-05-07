# downloadarx's setup.py
#from distutils.core import setup
from setuptools import setup
setup(
    name = "downloadarx",
    packages = ["downloadarx"],
    version = "1.0.0",
    description = "Download DLI Telugu catalog",
    author = "Arjuna Rao Chavala ",
    author_email = "arjunaraoc@gmail.com",
    url = "https://github.com/arjunaraoc/downloadarx",
    download_url = "https://github.com/arjunaraoc/downloadarx",
    keywords = ["catalog", "archive.org", "DLI"],
    install_requires=[
        'requests'
    ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
to download Telugu DLI books catalog from collection Digitallibraryindia
"""
)