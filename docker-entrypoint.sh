#!/bin/sh
cd /app
pip3 install flask
pip3 install functools
export FLASK_RUN_PORT=9292
flask --app fakelastic run --debug  --host=0.0.0.0