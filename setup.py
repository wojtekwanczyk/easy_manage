import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

requirement_list = [
    'argparse',
    'redfish',
    'pymongo',
    'pymongo[srv]'
]

setuptools.setup(
    name="easy_manage",
    version="0.0.1",
    author="Borkowski Szymek, Rejowski Tomek, Wanczyk Wojtek",
    author_email="boro@email.com, tomek@email.com, wojtekwanczyk@gmail.com",
    description="Managing server infrastructure easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wojtekwanczyk/easy_manage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'easy_manage = easy_manage.easy_manage:main']
    },
    install_requires=requirement_list
)
