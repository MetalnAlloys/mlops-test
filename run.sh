#!/bin/bash

KUSTOMIZE_DIR="./kustomize"

# Setting these here just for example running of the script. 
# These env vars should be created separately/secretly 
export GOOGLE_ARTIFACTS_REG="a.dev"
export NAMESPACE="mlops"
export VERSION="0.0.1"
export RUN_MODE="dev"
export DJANGO_SUPERUSER_PASSWORD="admin123"
export POSTGRES_PASSWORD="admin123"
export MLOPS_DB_NAME="mlops_db"
export MLOPS_DB_PASS="admin123"
export MLOPS_DB_USER="mlops_user"
export MLOPS_DB_HOST="mlops-db"


# Enter the minikube docker deamon for local dev mode
if [ "$RUN_MODE" == "dev" ] ; then
    eval $(minikube docker-env)
fi

case "$1" in
    run)
        kubectl create namespace "$NAMESPACE"
        kubectl kustomize kustomize/overlays/$RUN_MODE | envsubst | kubectl apply -n "$NAMESPACE" -f-
        ;;
    stop)
        kubectl kustomize kustomize/overlays/$RUN_MODE | kubectl delete -n "$NAMESPACE" -f-
        kubectl delete namespace "$NAMESPACE"
        ;;
    build)
        if [ "$2" == "" ] || [ "$2" == "backend" ]; then
            docker build -f ./Dockerfile_backend -t "mlops:$VERSION" .
        fi
        
        if [ "$2" == "" ] || [ "$2" == "nginx" ]; then
            docker build -t "mlops-nginx:$VERSION" -f Dockerfile_nginx .
        fi
        ;;
    *)
        cat <<EOF
Usage:
======

run.sh run
Deploy the containers to a kubernetes distribution

run.sh build [image]
build/rebuild the "image" Or builds all if run without arguments

EOF
    ;;
esac





