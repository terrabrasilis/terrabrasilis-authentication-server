#!/bin/bash

#source env/bin/activate

cd api

gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app
