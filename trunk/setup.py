try:
    from setuptools import setup
except:
    from distutils.core import setup

import forms

setup(
    name='forms',
    version=forms.version,
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=['forms', 'forms.test'],
    package_data={
        'forms': ['forms.css'],
        }
    )
