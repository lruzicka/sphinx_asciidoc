"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='sphinx-asciidoc',  # Required
    version='0.9.0',  # Required
    description='A custom Sphinx builder to make asciidoc output',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/lruzicka/sphinx-asciidoc',  # Optional
    author='Lukáš Růžička',  # Optional
    author_email='lukas.ruzicka@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    keywords='sphinx extension builder asciidoc',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=['sphinx'],  # Optional

    entry_points={  # Optional
        'sphinx.builders': [
            'asciidoc = asciidoc:AsciiDocBuilder',
        ],
    },
)

