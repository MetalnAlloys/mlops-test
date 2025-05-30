#!/bin/bash

KUSTOMIZE_DIR="./kustomize"

#--------------------------------------------------------------
# Configration
#
# NOTE:
#   Setting these here just for example running of this script. 
#   These env vars should be created separately/secretly 
#   e.g. fetched from a GCP secret or a GCS bucket
#---------------------------------------------------------------
export NAMESPACE="mlops"
export VERSION="0.0.1"
export RUN_MODE="dev"
export POSTGRES_PASSWORD="admin123"
export MLOPS_DB_NAME="mlops_db"
export MLOPS_DB_PASS="admin123"
export MLOPS_DB_USER="mlops_user"
export MLOPS_DB_HOST="mlops-db"
export PIPELINE="test_pipeline.joblib"
# these two are needed for running in 'prod'
export STATIC_FILES_GCS_BUCKET="add-some-gcs-bucket"
export GOOGLE_ARTIFACTS_REG="europe-west1-docker.pkg.dev/registry/"



# -------------------------------------------
# Wrapper funtion to build docker containers
# -------------------------------------------
build_container() {
    local DOCKER_IMAGE="$1"
    local DOCKERFILE="$3"
    local CONTEXT="${4:-.}"

    args=()
    args+=(-f "$DOCKERFILE")

    if [ "$2" == "prod" ]; then
        args+=(--tag "$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE:$VERSION")
        # TODO: enable Docker buildkit for caching
        #args+=(--cache-from "type=registry,ref=$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE-cache,mode=max")
        #args+=(--cache-to "type=registry,ref=$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE-cache,mode=max")
    else
        args+=(--tag "$DOCKER_IMAGE:$VERSION")
    fi

    args+=("$CONTEXT")

    docker build "${args[@]}"
    if [ "$2" == "prod" ]; then
        docker push "$GOOGLE_ARTIFACTS_REG/$DOCKER_IMAGE:$VERSION"
    fi
}


# Enter the minikube docker deamon for local dev mode
if [ "$RUN_MODE" == "dev" ] ; then
    eval $(minikube docker-env)
fi


#------------------
# Commands section
#------------------

case "$1" in
    db)
        bash ./init-db.sh | envsubst
        ;;
    run)
        kubectl create namespace "$NAMESPACE"
        kubectl kustomize kustomize/overlays/$RUN_MODE | envsubst  | kubectl apply -n "$NAMESPACE" -f-
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
run.sh db
Initialize an empty Postgres DB

run.sh run
Deploy the containers to a kubernetes distribution

run.sh build [image]
build the docker [image] Or builds all if run without arguments

EOF
    ;;
esac





