#!/bin/sh
set -e

RED='\033[0;31m' 
NC='\033[0m'

if [ -e ./spark-submit-dependencies/bin/spark-submit ]; then
    echo "spark-submit was found!"
else
    echo -e "spark-submit was not found in ./spark-submit-dependencies/bin/. Please open your terminal and run ${RED} bash ./get-spark-submit-dependencies.sh${NC} from the projects home directory to get spark-submit."
    exit 1
fi

minikube start
eval $(minikube docker-env)

bash build-pyspark.sh

minikube addons enable ingress
minikube addons enable ingress-dns

# todo: figure out why my custom role isn't working
# kubectl apply -f ./k8s/spark-driver-service-account.yaml
# kubectl apply -f ./k8s/spark-driver-role.yaml
# kubectl apply -f ./k8s/spark-driver-role-binding.yaml
# --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-driver-account \

kubectl delete clusterrolebinding default --ignore-not-found
kubectl create clusterrolebinding default --clusterrole=edit --serviceaccount=default:default --namespace=default

# # todo - get control pane address in variable
kubectl cluster-info

./spark-submit-dependencies/bin/spark-submit \
    --master k8s://https://127.0.0.1:51950 \
    --deploy-mode cluster \
    --name pyspark-job \
    --executor-memory 4G \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=pyspark:latest \
    --conf spark.kubernetes.container.image.pullPolicy=Never \
    local:///opt/spark/work-dir/app-pyspark/main.py
