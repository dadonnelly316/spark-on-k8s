#!/bin/sh
set -e

POSTGRES_CONN_ID=${1}
POSTGRES_PASSWORD=${2}
S3_KEY_ID=${3}

kubectl delete secret hive-metastore-secrets --ignore-not-found

kubectl create secret generic hive-metastore-secrets \
    --type=string \
    --from-literal=postgres-connection-url=${POSTGRES_CONN_ID} \
    --from-literal=postgres-password=${POSTGRES_PASSWORD} \
    --from-literal=s3-key-id=${S3_KEY_ID} \
    --from-literal=s3-key-secret=${S3_KEY_SECRET}