from setuptools import setup, find_packages

import formal

setup(
    name='formal',
    version=formal.version,
    description='HTML forms framework for Nevow',
    author='Matt Goodall',
    author_email='matt@pollenation.net',
    packages=find_packages(),
    package_data={
        'formal': ['formal.css', 'html/*', 'js/*'],
        },
    zip_safe = True,
    )
