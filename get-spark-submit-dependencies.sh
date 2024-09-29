#!/bin/sh
set -e

cd ./spark-submit-dependencies && { curl -O  https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz ; cd -; }

tar -xvzf ./spark-submit-dependencies/spark-3.5.3-bin-hadoop3.tgz --exclude='README.md' --strip-components=1 -C ./spark-submit-dependencies