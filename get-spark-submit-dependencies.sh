#!/bin/sh
set -e

# todo: do i even need to downlaod spark? Can i just override the spark image entrypoint to run the spark-submit executable, which in turn would spark the driver?
# todo: think if this should be left in project's home dir to make its location evident, or to move it to a util scripts folder to clean up home dir

cd ./spark-submit-dependencies && { curl -O  https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz ; cd -; }

tar -xvzf ./spark-submit-dependencies/spark-3.5.3-bin-hadoop3.tgz --exclude='README.md' --strip-components=1 -C ./spark-submit-dependencies