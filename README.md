# The HuBMAP Registration Portal

## Installation

Install [Pipenv](https://docs.pipenv.org/en/latest/)

## activate env
```pipenv shell```

You may see the following:

````
[zhy19@localhost registration]$ pipenv shell
Warning: Python 3.6 was not found on your system…
You can specify specific versions of Python with:
  $ pipenv --python path/to/python
[zhy19@localhost registration]$ which python3
/usr/bin/python3
[zhy19@localhost registration]$ pipenv --python /usr/bin/python3
Creating a virtualenv for this project…
Pipfile: /home/zhy19/HuBMAP/registration/Pipfile
Using /usr/bin/python3 (3.7.3) to create virtualenv…
⠧ Creating virtual environment...Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/zhy19/.local/share/virtualenvs/registration-q6hMIbP1/bin/python3
Also creating executable in /home/zhy19/.local/share/virtualenvs/registration-q6hMIbP1/bin/python
Installing setuptools, pip, wheel...done.

✔ Successfully created virtual environment! 
Virtualenv location: /home/zhy19/.local/share/virtualenvs/registration-q6hMIbP1
Warning: Your Pipfile requires python_version 3.6, but you are using 3.7.3 (/home/zhy19/.local/share/v/r/bin/python).
  $ pipenv --rm and rebuilding the virtual environment may resolve the issue.
  $ pipenv check will surely fail.
[zhy19@localhost registration]$ 
````

Then install all the dependencies:

````
pipenv install
````

## run flask development server
```
export FLASK_APP=hello.py
export FLASK_ENV=development
flask run
```