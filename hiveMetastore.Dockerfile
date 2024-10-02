FROM apache/hive:4.0.0

USER 0

RUN apt-get update && apt-get upgrade -y

COPY ./hive-metastore/metastore-site.xml ${HIVE_HOME}/conf

# todo - make sure i'm dropping the postgres driver in the right folder
COPY ./maven-dependencies/hive-metastore ${HIVE_HOME}/lib

ENV DB_DRIVER=postgres
ENV SERVICE_NAME=metastore

ARG HIVE_USER=1000
USER ${HIVE_USER}