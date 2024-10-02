#!/bin/sh
set -e

# todo - how to configure terraform to make sure hive metastore is automatically opened to EC2 where K8s is on EKS
# todo: must create new security group, not modify existing : https://stackoverflow.com/questions/37212945/aws-cant-connect-to-rds-database-from-my-machine
# note - i think i need an outbound rule on my rds 
# https://stackoverflow.com/questions/35655306/hive-installation-issues-hive-metastore-database-is-not-initialized
# todo: check if my subnet is correctly set up : https://serverfault.com/questions/835742/connection-timed-out-on-new-aws-rds-instances-can-connect-to-older-almost-ide
# todo - offload logs outside of pod?
# todo: do i need to mount volumes?

mvn dependency:copy-dependencies -f pom-hive-metastore.xml -DoutputDirectory=./maven-dependencies/hive-metastore/

# todo - maybe dockerfiles should sit somewhere else and we make the project's home directory the build `context`

docker build \
    --pull \
    --tag hive-metastore \
    --file hiveMetastore.Dockerfile \
    --progress=plain \
    .