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

minikube start --cpus 4 --memory 7000
eval $(minikube docker-env)

kubectl config set-cluster minikube
minikube config view vm-driver

# minikube ssh -- docker system prune # run this if out of disk space

rm ./maven-dependencies/hive-metastore/*
rm ./maven-dependencies/spark/*

bash build-pyspark.sh
# todo: need a better way to configure the image pull policy
bash build-hive-metastore.sh

minikube addons enable ingress
minikube addons enable ingress-dns

# todo: figure out why my custom role isn't working
# kubectl apply -f ./k8s/spark-driver-service-account.yaml
# kubectl apply -f ./k8s/spark-driver-role.yaml
# kubectl apply -f ./k8s/spark-driver-role-binding.yaml
# --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-driver-account \

kubectl apply -f ./k8s/hive-metastore-deployment.yaml
kubectl apply -f ./k8s/hive-metastore-service.yaml

kubectl wait --for=condition=ready pod -l app=hive-metastore

kubectl delete clusterrolebinding default --ignore-not-found
kubectl create clusterrolebinding default --clusterrole=edit --serviceaccount=default:default --namespace=default

kubectl apply -f ./k8s/spark-submit-pod.yaml
# kubectl get event --namespace default --field-selector involvedObject.name=spark-submit
