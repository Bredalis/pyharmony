#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import necessary modules
import os
import sys

# Function to resolve path relative to the script's location
here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

try:
    from setuptools import setup  # Use setuptools if available
except ImportError:
    from distutils.core import setup  # Otherwise, fallback to distutils

# Handling the 'publish' argument for uploading the package
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')  # Run sdist and upload to PyPI
    sys.exit()  # Exit after publishing

# Read the README file for the long description of the package
readme = open(here('README.md')).read()
# Get package requirements from requirements.txt file
requirements = [x.strip() for x in open(here('requirements.txt')).readlines()]

# Setup configuration
setup(
    name='pyharmony',  # Package name
    version='1.0.20',  # Package version
    description='Python library for programmatically using a Logitech Harmony Link or Ultimate Hub.',  # Package description
    long_description=readme,  # Long description from README file
    author='Ian Day',  # Author's name
    author_email='ian236day@gmail.com',  # Author's email
    url='https://github.com/iandday/pyharmony',  # Project URL
    download_url='https://github.com/iandday/pyharmony/tarball/1.0.20',  # URL for downloading specific versions
    packages=['pyharmony'],  # List of packages
    package_dir={'pyharmony': 'pyharmony'},  # Directory structure
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    install_requires=requirements,  # Dependencies
    license="BSD",  # License information
    zip_safe=False,  # Don't zip the installed package
    keywords='pyharmony',  # Keywords associated with the package
    classifiers=[  # Classifiers for the package
        'Development Status :: 4 - Beta',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={  # Entry points for console scripts
        'console_scripts': [
            'harmony = pyharmony.__main__:main'
        ]
    },
)
