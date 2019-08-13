# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in er_diagram/__init__.py
from er_diagram import __version__ as version

setup(
	name='er_diagram',
	version=version,
	description='Generate ER-Diagrams for DocTypes',
	author='Steffen Brennscheidt',
	author_email='steffen@brennscheidt.net',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
