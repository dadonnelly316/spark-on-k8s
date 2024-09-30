#!/bin/sh
set -e

terraform init
terraform plan

echo "provisioning infrastructure"
echo "yes" | terraform apply

