"lacrm package setup"

from setuptools import setup

setup(
    name="lacrm",
    version="0.1.1",
    maintainer="Ryan Sellers",
    maintainer_email="curiouschiblog@gmail.com",
    packages=["lacrm"],
    url="https://github.com/HighMileage/lacrm",
    description=("lacrm is a basic lessannoyingcrm.com REST API client. "
                 "The goal is to provide an easy to use interface for the "
                 "LACRM API."),
    keywords="lacrm less annoying CRM lessannoyingcrm.com",
)
