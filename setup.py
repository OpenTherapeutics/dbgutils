import os, sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)

with open('README.md') as f:
    long_description = f.read()


VERSION = __import__('dbgutils').get_version()

setup(
    name='dbgutils',
    version=VERSION,
    url='https://github.com/dakrauth/dbgutils',
    author='David A Krauth',
    author_email='dakrauth@gmail.com',
    description='Basic collection of common debugging tools for Python and various apps.',
    long_description=long_description,
    platforms=['any'],
    license='MIT License',
    classifiers=(
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ),
    packages=find_packages(),
)
