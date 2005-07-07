try:
    from setuptools import setup
except:
    from distutils.core import setup
from distutils.command import install

import forms

for scheme in install.INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='forms',
    version=forms.version,
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=['forms', 'forms.test'],
    data_files=[
        ['forms', ['forms/forms.css']],
        ]
    )
