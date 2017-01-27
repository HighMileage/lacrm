"lacrm package setup"

import os
from setuptools import setup

def read_version():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'lacrm',
        '_version.py'
    )
    with open(path) as f:
        exec(f.read())
        return locals()['__version__']

def download_url():
    return 'https://github.com/highmileage/lacrm/tarball/{0}'.format(
        read_version())

setup(
    name="lacrm",
    version=read_version(),
    maintainer="Ryan Sellers",
    maintainer_email="curiouschiblog@gmail.com",
    packages=["lacrm"],
    download_url=download_url(),
    url="https://github.com/HighMileage/lacrm",
    description=("lacrm is a basic lessannoyingcrm.com REST API client. "
                 "The goal is to provide an easy to use interface for the "
                 "LACRM API."),
    keywords="lacrm less annoying CRM lessannoyingcrm.com",
    install_requires=[
        'requests[security]',
    ]
)
