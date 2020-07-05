"""Setup tools packaging information."""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    "requests",
    "pytest",
    "coverage",
    "mongoengine",
    "bs4",
    "Unidecode",
    "telegram"
]

open(os.path.join(here, "requirements.txt"), "w").writelines(
    [line + "\n" for line in requires]
)

setup(
    name="digispider",
    version="20191220",
    description="Digikala Utility",
    long_description="This utility is intended to ease the awareness of new orders on Digikala",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author="Alireza Hoseini",
    author_email="alireza.stack@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""\
    [console_scripts]
    ds_fetch = digispider.fetch:main
    """,
)
