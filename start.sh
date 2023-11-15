#!/bin/bash
gunicorn -c gunicorn_config.py main_safe_flask:app & 
python3 all.py
