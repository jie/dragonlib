# -*- coding: utf-8 -*-
"""
    Tornado utils
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name = "dragonlib",
    version = "0.1.1",
    packages = find_packages(),

    install_requires = [
        "addict==2.2.1",
        "celery==4.4.6",
        "coverage==5.2",
        "Jinja2==2.11.3",
        "nose2==0.9.2",
        "redis==3.5.3",
        "requests==2.24.0",
        "shortuuid==1.0.1",
        "tornado==6.0.4",
        "xlwt==1.3.0",
    ],

    author = "zhouyang",
    author_email = "zhouyang@zhouyang.me",
    description = "Tornado utils",
    license = "BSD",
    keywords = "torndao, utils",
    url = "https://github.com/jie/dragonlib",
)
