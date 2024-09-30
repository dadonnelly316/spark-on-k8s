#!/bin/sh
set -e

AWS_API_KEY=${1}
AWS_API_SECRET=${2}

kubectl create secret generic aws-login --type=string --from-literal=aws-access-key-id=${AWS_API_KEY} --from-literal=aws-secret-access-key=${AWS_API_SECRET}

