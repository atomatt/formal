from setuptools import setup, find_packages

setup(
    name='formal',
    version='0.8.1',
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=find_packages(),
    package_data={
        'formal': ['formal.css', 'html/*', 'js/*'],
        },
    zip_safe = True,
    )
