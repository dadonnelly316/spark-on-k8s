#!/bin/sh
set -e

# maven shouldn't be in the runtime environment. Ideally Maven would be installed in your CI/CD environment
mvn dependency:copy-dependencies -f pom-pyspark.xml -DoutputDirectory=./maven-dependencies/spark/

docker build \
    --pull \
    --tag pyspark \
    --file pyspark.Dockerfile \
    --progress=plain \
    .