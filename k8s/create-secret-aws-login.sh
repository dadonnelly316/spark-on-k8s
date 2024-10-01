#!/bin/sh
set -e

AWS_API_KEY=${1}
AWS_API_SECRET=${2}
S3_BUCKET_NAME=${3}

kubectl delete secret aws-login --ignore-not-found

kubectl create secret generic aws-login \
    --type=string \
    --from-literal=aws-access-key-id=${AWS_API_KEY} \
    --from-literal=aws-secret-access-key=${AWS_API_SECRET} \
    --from-literal=s3-bucket-name=${S3_BUCKET_NAME} \

