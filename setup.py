"""Setup file for the MPipe module."""

from setuptools import setup


with open('./src/version.py') as f:
    exec(f.read())

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='mpipe',
    version=__version__,
    url='http://vmlaker.github.io/mpipe',
    author='Velimir Mlaker',
    author_email='velimir.mlaker@gmail.com',
    license='MIT',
    description='Multiprocess pipeline toolkit',
    long_description=long_description,
    package_dir={'mpipe' : 'src'},
    packages=['mpipe'],
    setup_requires=[
        'pytest-runner==4.4',
    ],
    tests_require=[
        'pytest==4.5.0',
    ],
    classifiers=[
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
