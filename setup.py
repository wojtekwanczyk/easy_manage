import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS_LIST = [
    'redfish >= 2.1.0',
    'pymongo[srv] >= 3.8.0',
    'python-ipmi >= 0.4.1',
    'cryptography >= 2.7'
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
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'easy_manage = easy_manage.__init__:main']
    },
    install_requires=REQUIREMENTS_LIST
)
