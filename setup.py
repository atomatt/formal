from setuptools import setup, find_packages

import forms

setup(
    name='forms',
    version=forms.version,
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=find_packages(),
    package_data={
        'forms': ['forms.css'],
        }
    )
