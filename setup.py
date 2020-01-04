"easy_manage setup file"

import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS_LIST = [
    'redfish >= 2.1.0',
    'cryptography >= 2.7',
    'python-ipmi',
    'paramiko >= 2.6.0',
    'inflection >= 0.3.1',
]

setuptools.setup(
    name="easy_manage",
    version="0.0.1",
    author="Borkowski Szymus, Rejowski Tomus, Wanczyk Wojtek",
    author_email="borkowskiszymon28@gmail.com, tomekgsd@gmail.com, wojtekwanczyk@gmail.com",
    description="Managing server infrastructure easily",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/wojtekwanczyk/easy_manage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'easy_manage = easy_manage.__init__:main']
    },
    dependency_links=[
        'http://github.com/Arcticae/python-ipmi/tarball/master#egg=python-ipmi-0'
    ],
    install_requires=REQUIREMENTS_LIST
)
