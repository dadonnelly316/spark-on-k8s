#!/bin/sh
set -e

YELLOW='\033[0;33m' 
NC='\033[0m'

minikube start --cpus 4 --memory 7000
eval $(minikube docker-env)

kubectl config set-cluster minikube
minikube config view vm-driver

# minikube ssh -- docker system prune # run this if out of disk space

rm ./maven-dependencies/hive-metastore/*
rm ./maven-dependencies/spark/*

bash build-pyspark.sh
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

echo -e "${YELLOW}Make sure the clusterIP of your K8s cluster is passed in the --master option of spark submit. Do not pass the control pane IP.${NC}"
kubectl delete pod spark-submit --ignore-not-found
kubectl apply -f ./k8s/spark-submit-pod.yaml
# kubectl get event --namespace default --field-selector involvedObject.name=spark-submit
