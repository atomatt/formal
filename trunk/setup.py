from setuptools import setup, find_packages

setup(
    name='formal',
    version='0.12.0',
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=find_packages(),
    include_package_data=True,
    zip_safe = True,
    )
