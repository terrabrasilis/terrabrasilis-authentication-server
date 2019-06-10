
## virtualenv

### Configuration file

nano ~/.virtualenv/virtualenv.ini

```sh

# create virtual env inside a pwd path
virtualenv env

# use one python version
virtualenv --python=/usr/bin/python3 env

# to activate the virtual env
source env/bin/activate

# to leave
deactivate

```

```sh
# To generate the package installed list
pip freeze -l > utils/requirements.txt
```

## To run using gunicorn use:

```sh
gunicorn -k eventlet -w 1 -b 127.0.0.1:5000 wsgi:app

# this will start in port: 8000
gunicorn --worker-class eventlet -w 1 wsgi:app
```