from setuptools import setup, find_packages

version = '0.18.2'

with open("README.md", "r") as fh:
    long_description = fh.read()


import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

name = 'qtwidgets'
extra_files = package_files(os.path.join(os.path.dirname(__file__), name))

setup(
    name=name,
    version=version,
    author='Martin Fitzpatrick',
    author_email='martin.fitzpatrick@gmail.com',
    description='Custom widget library for PyQt5 and PySide2 (Qt for Python). Free to use in your own applications.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/learnpyqt/python-qtwidgets',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={'':extra_files},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Widget Sets',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ]
)
