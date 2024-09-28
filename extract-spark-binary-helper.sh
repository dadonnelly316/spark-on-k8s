#!/bin/sh
set -e

# todo: curl to grab spark binary and download to spark-binaries

# You must bring your own local spark binary in order to run spark-submit, and make sure it's in the right directory. This helper function attempts to grab it for you.
tar -xvzf ./spark-binaries/spark-3.5.3-bin-hadoop3.tar --exclude='README.md' --strip-components=1 -C ./spark-binaries