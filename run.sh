#!/bin/bash

KUSTOMIZE_DIR="./kustomize"

# Setting these here just for example running of the script. 
# These env vars should be created separately/secretly 
# e.g. fetched from a gcloud secret or GCS bucket
export GOOGLE_ARTIFACTS_REG="xxx-docker.pkg.dev/project/registry"
export NAMESPACE="mlops"
export VERSION="0.0.1"
export RUN_MODE="prod"
export DJANGO_SUPERUSER_PASSWORD="admin123"
export POSTGRES_PASSWORD="admin123"
export MLOPS_DB_NAME="mlops_db"
export MLOPS_DB_PASS="admin123"
export MLOPS_DB_USER="mlops_user"
export MLOPS_DB_HOST="mlops-db"



##########################################
# Wrapper func. to build docker containers
build_container() {
    local DOCKER_IMAGE="$1"
    local DOCKERFILE="$3"

    context="${4:-.}"

    args=()
    args+=(--tag "$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE:$VERSION")
    args+=(-f "$DOCKERFILE")

    if [ "$2" == "prod" ]; then
        args+=(--push)
        # TODO: enable Docker buildkit for caching
        #args+=(--cache-from "type=registry,ref=$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE-cache,mode=max")
        #args+=(--cache-to "type=registry,ref=$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE-cache,mode=max")
    fi

    args+=("$context")

    docker build "${args[@]}"
    if [ "$2" == "prod" ]; then
        docker push "$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE:$VERSION"
    fi
}


# Enter the minikube docker deamon for local dev mode
if [ "$RUN_MODE" == "dev" ] ; then
    eval $(minikube docker-env)
fi


case "$1" in
    run)
        kubectl create namespace "$NAMESPACE"
        kubectl kustomize kustomize/overlays/$RUN_MODE | envsubst #| kubectl apply -n "$NAMESPACE" -f-
        ;;
    stop)
        kubectl kustomize kustomize/overlays/$RUN_MODE | kubectl delete -n "$NAMESPACE" -f-
        kubectl delete namespace "$NAMESPACE"
        ;;
    build)
        if [ "$2" == "" ] || [ "$2" == "backend" ]; then
            build_container mlops "$RUN_MODE" Dockerfile_backend 
        fi
        
        if [ "$2" == "" ] || [ "$2" == "nginx" ]; then
            build_container mlops-nginx "$RUN_MODE" Dockerfile_nginx 
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





