FROM apache/spark:3.5.3-scala2.12-java17-python3-r-ubuntu

ARG spark_uid=185
USER 0

RUN apt-get update && apt-get upgrade -y

COPY ./app-pyspark ./app-pyspark
COPY ./maven-dependencies ${SPARK_HOME}/jars
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

# Must set progress=plain in docker build to see output
RUN echo ${SPARK_HOME}
RUN pwd

USER ${spark_uid}
