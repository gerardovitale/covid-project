#!/bin/bash

# run pipeline-spark_app
python app.py

# start jupyter notebook
jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root