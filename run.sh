#!/bin/sh
mkdir ~/.kaggle
cp ./kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

jupyter-lab --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token="kaggle" --notebook-dir=/kaggle