from setuptools import setup, find_packages

setup(
    name='formal',
    version='0.9.1',
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=find_packages(),
    package_data={
        '': ['*.css', '*.html', '*.js'],
        },
    zip_safe = True,
    )
