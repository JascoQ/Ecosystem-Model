#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 20:16:26 2020

@author: glatt
"""

import os
from setuptools import setup
import re, pathlib

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)

def get_requirements():
    reqpath = pathlib.Path("./requirements.txt")
    reqs = reqpath.read_text().splitlines()
    return reqs


project_name = "Ecosystem_Simulation-JascoQ"

setup(
    name = project_name,
    version = "1.0.0",
    author = "Giovanni Marangi",
    author_email = "giovanni.marangi@studio.unibo.it",
    description = ("Two different approaches to simulate an ecosystem"),
    #license = "Unlicense",
    keywords = "Ecosystem, foodwebs, migration flux",
    url = "https://github.com/JascoQ/Ecosystem-Model",
    packages=['IBM','DCM'],
    #packages=setuptools.find_packages(),
    #install_requires= get_requirements(),
    install_requires=['networkx==2.3',
		      'numpy==1.16.2',
		      'scipy==1.10.0',
		      'matplotlib==3.0.3'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
