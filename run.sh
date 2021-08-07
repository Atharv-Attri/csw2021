#!/bin/bash

sudo apt-get install libzbar0 --force-yes
pip install -r requirements.txt
export FLASK_APP=index.py
export FLASK_ENV=development
flask run
gp url 5000