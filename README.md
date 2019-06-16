# easy-manage :fish:

## Important links 	:star:

[Praca inżynierska]: https://www.overleaf.com/7868136442hhzxfsqkxmtw

[Documents](https://drive.google.com/open?id=1EreYxAh-ETU-srL9644vSiHSea4uAuf4)

[IPMI pdf doc](http://openipmi.sourceforge.net/IPMI.pdf)

[IPMI intel doc](https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/ipmi-second-gen-interface-spec-v2-rev1-1.pdf)

## Schedule 	:anger:
![Plan](https://github.com/wojtekwanczyk/easy-manage/blob/master/resources/schedule.jpg)



## Project configuration :art:

Remember to work within python virtual environment.
Pycharm creates one for you if you didn't unmark something like
`create virtual environment for this project` while loading project.

Virtualenv usually kept in directory named `venv` or `env` in the project root directory.
If you don't have one see `Create virtualenv` :golf:

#### Create virtualenv :golf:
I recommend using virtualnv but you can use pyvenv or anaconda. Got to root
directory and type `virtualenv <venv_dir_name>` e.g. `virtualenv venv`. It will create virtual environment
with your default python version. To use different python version, you need to download one and use `-p PYTHON_EXE` or ` --python=PYTHON_EXE` flag e.g. 
`-p c:\users\wwojciec\appdata\local\programs\python\python37\python.exe` On linux pythons are usually stored under `/usr/bin/python`. Be careful there! :snake:

#### Check virtualenv :trumpet:
To check python version type `python --version` or `which python`. You should also check if everything is alright with pip with the same commands. If python from root directory folder is not used, you must activate virtualenv :droplet:


#### Activate and deactivate virtualenv :droplet:
If python is not used from venv in project root directory you need to activate your venv.
__Remember that PyCharm does that for you!__ To make sure before activating/deactivating venv always
check virtualenv. :trumpet: Go to project root directory with venv in it and type

Windows: `source venv/Scripts/activate`

Linux: `source venv/bin/activate`

Deactivation (both): `deactivate`

Quite simple :boom:


#### Install requirements :pencil2:
Remember to use `pip install -r requirements.txt`. That's the fastest way to get all packages you need to your fresh and crunchy virtual environment.


#### Build and use wheel package :trophy:
To build package using `setuptools` type `python setup.py build`. You can type 
`python setup.py install` command which builds the package too, but also install it in your environment.
Now you can use it from command line e.g. `easy_manage`. That's the beauty of it. :zap:

## Less important links :dromedary_camel:

[to2 template](https://trac.iisg.agh.edu.pl/to2/wiki/TemplateProject/Wizja)
