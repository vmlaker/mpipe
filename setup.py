"""Setup file for the MPipe module."""

from setuptools import setup


exec(open('./src/version.py').read())

setup(
    name         = 'mpipe',
    version      = __version__,
    description  = 'Multiprocess pipeline toolkit',
    url          = 'http://vmlaker.github.io/mpipe',
    author       = 'Velimir Mlaker',
    author_email = 'velimir.mlaker@gmail.com',
    license      = 'MIT',
    long_description = open('README.rst').read(),
    package_dir  = {'mpipe' : 'src'},
    packages     = ['mpipe'],
    setup_requires=[
        'pytest-runner==4.4',
    ],
    tests_require=[
        'pytest==4.5.0',
    ],
    classifiers  = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
