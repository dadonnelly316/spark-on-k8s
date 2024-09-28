#!/bin/sh
set -e

# maven shouldn't be in the runtime environment. Ideally Maven would be installed in your CI/CD environment
mvn dependency:copy-dependencies -DoutputDirectory=./maven-dependencies/

docker build \
    --pull \
    --tag pyspark \
    --file pyspark.Dockerfile \
    --progress=plain \
    .