# mlops-test

MLOps example setup that includes;

1. A Python Django based backend 
2. REST API created using DRF (Django Rest Framework)
3. Nginx as a reverse proxy
3. Kubernetes deployment using Kustomize overlays
4. CI/CD setup using Github Actions
5. Various helper shell scripts


## How to run locally (dev mode)

In order to run locally, the following binaries are required;

1. [minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
2. [kubectl](https://kubectl.docs.kubernetes.io/)
3. A running Docker daemon
3. It also requires a small tool called `envsubst` but it is assumed as
   pre-installed on a standard Linux


#### Step 1: Start minikube
- Clone this repo and execute the following command from its root:

    ```sh
    minikube start --driver=docker --mount --mount-string="${PWD}:/host" --ports=80:80,443:443
    ```
- Run the following to enable ingress API
    ```sh
    minikube addons enable ingress
    ```


#### Step 2: Configure
- Setup requires some environment variables. See/edit the configration section
    (lines 13 ro 23) in the `run.sh` script. For a demo run, the defaults are good enough.
- Available environment variables:
    + __NAMESPACE:__ Kubernetes namespace to deploy the resources in
    + __VERSION:__ Docker images version tag
    + __RUN_MODE:__ 'dev' or 'prod' (use dev here)
    + __POSTGRES_PASSWORD:__ root 'postgres' user password
    + **MLOPS_DB_*:**  All these are needed to setup the database. See
    `./ml_server/ml_server/settings.py` for usage
    + __STATIC_FILES_GCS_BUCKET:__ A GCS bucket used to serve static files in
        'prod'
    + __GOOGLE_ARTIFACTS_REG:__ Online storage for built docker images. Useful
        for 'prod' mode


### Step 3: Build docker images
- Run to build the backend and nginx docker images

    ```sh
    bash run.sh build

    ```


### Step 4: Run
- Run the following and wait for the kubernetes Deployment to complete

    ```sh
    bash run.sh run
    ```


Thats it! The app should be available at `http://localhost`



### How to run in production (prod mode)

In order to deploy to production, make sure the following resources are available;
1. A GKE cluster accessible through `kubectl`
2. A Google artifacts registry. Subsitute as __GOOGLE_ARTIFACTS_REG__
3. A GCS bucket for storing static files. Subsitute as __STATIC_FILES_GCS_BUCKET
4. Set _RUN_MODE_ environment variable to `prod`


#### Step 1: Build docker images
- `bash run.sh build`


#### Step 2: Deploy
- `bash run.sh run`



Get nginx IP using;

```bash
    IP=$(kubectl get svc nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

Navigate to http://$IP
