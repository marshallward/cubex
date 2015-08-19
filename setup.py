"""setup.py
   ========
   Installation script for cubex

   Additional configuration settings are in ``setup.cfg``.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

project_name = 'cubex'
project_version = __import__(project_name).__version__
project_readme_fname = 'README.rst'

with open(project_readme_fname) as f:
    project_readme = f.read()

setup(
    name = project_name,
    version = project_version,
    description = 'CUBE .cubex library parser',
    long_description = project_readme,
    author = 'Marshall Ward',
    author_email = 'cubex@marshallward.org',
    url = 'http://github.com/marshallward/cubex',

    packages = ['cubex'],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ]
)
