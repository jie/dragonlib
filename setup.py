# -*- coding: utf-8 -*-
"""
    Tornado utils
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name = "aiohttp-babel",
    version = "0.0.6",
    packages = find_packages(),

    install_requires = [
        "addict==2.2.1",
        "amqp==2.5.0",
        "arrow==0.4.2",
        "asn1crypto==0.24.0",
        "billiard==3.6.0.0",
        "cached-property==1.5.1",
        "captcha==0.3",
        "celery==4.3.0",
        "certifi==2019.6.16",
        "cffi==1.12.3",
        "chardet==3.0.4",
        "contextlib2==0.5.5",
        "coverage==4.5.3",
        "cryptography==2.7",
        "defusedxml==0.6.0",
        "dnspython==1.16.0",
        "exchangelib==1.12.5",
        "future==0.17.1",
        "gevent==1.4.0",
        "greenlet==0.4.15",
        "gunicorn==19.9.0",
        "ics==0.4",
        "idna==2.8",
        "isodate==0.6.0",
        "Jinja2==2.10.1",
        "kombu==4.6.3",
        "lxml==4.3.4",
        "MarkupSafe==1.1.1",
        "maxminddb==1.4.1",
        "nose2==0.9.1",
        "ntlm-auth==1.3.0",
        "Pillow==6.0.0",
        "pycparser==2.19",
        "pycrypto==2.6.1",
        "Pygments==2.4.2",
        "PyMySQL==0.9.3",
        "python-dateutil==2.8.0",
        "pytz==2019.1",
        "qiniu==7.2.4",
        "qrcode==6.1",
        "redis==3.2.1",
        "requests==2.22.0",
        "requests-ntlm==1.1.0",
        "schema==0.7.0",
        "shortuuid==0.5.0",
        "six==1.12.0",
        "tornado==6.0.2",
        "tzlocal==1.5.1",
        "urllib3==1.25.3",
        "vine==1.3.0",
        "xlwt==1.3.0",
        "yunpian-python-sdk==1.0.0"
    ],

    author = "zhouyang",
    author_email = "zhouyang@zhouyang.me",
    description = "Tornado utils",
    license = "BSD",
    keywords = "torndao, utils",
    url = "https://github.com/jie/dragonlib",
)