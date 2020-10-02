#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 20:16:26 2020

@author: glatt
"""

import os
from setuptools import setup
import re, pathlib

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)

def get_requirements():
    reqpath = pathlib.Path("./requirements.txt")
    reqs = reqpath.read_text().splitlines()
    return reqs


project_name = "Ecosystem_model"

setup(
    name = project_name,
    version = get_property('__version__', project_name),
    author = "Giovanni Marangi",
    author_email = "giovanni.marangi@studio.unibo.it",
    description = ("Two different approaches to simulate an ecosystem"),
    license = "Unlicense",
    keywords = "Ecosystem, foodwebs, migration flux",
    url = "https://github.com/JascoQ/Ecosystem-Model",
    packages=['IBM,DCM'],
    install_requires= get_requirements(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1.0",
        "Topic :: Ecosystem",
        "License :: Public Domain",
    ],
)