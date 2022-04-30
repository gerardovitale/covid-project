#!/bin/bash

# run pipeline-app
python -u app.py

# start jupyter notebook
jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
