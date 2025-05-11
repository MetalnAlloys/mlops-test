# mlops-test

MLOps example Pipeline setup 


## Pipeline architecture and design

__Worklow Cycle:__

Train ML Model → save to disk → serve as HTTP endpoint → predict 


### Components
1. Web server
- Django + DRF (Django Rest Framework) as a backend for serving predictions
- REST API:
    + `/api/v1/endpoints` list available endpoints
    + `/api/v1/algorithms` list registered algorithms
    + `/api/v1/requests` list all the processed requests
    + `/api/v1/lor/predict` run a prediction. (lor=logistic regression)


2. Proxy
- Nginx as a reverse proxy (See `nginx/nginx.conf`). Proxies the following:
- `/prometheus` to Prometheus server
- `/grafana` to the Grafana dashboard
- All other requests are proxied to the django backend at port 8000


3. Monitoring/Observability
- Prometheus to collect metrics. See `ml_server/ml_api/predict.py` for example
    usage on defining custom metrics
- Grafana to set up visual dashboards for metrics


4. Model Training
- A sample Logistic Regression model traing on Python Scikit Iris database


5. CI/CD Pipeline
- `./github/workflows/ci-pr.yaml` to run unit tests, retrain model and test deployment



## How to run locally (dev mode)

In order to run locally, the following binaries are required;

1. [minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
2. [kubectl](https://kubectl.docs.kubernetes.io/)
3. A running Docker daemon
4. It also requires a small tool called `envsubst` but it is assumed as
   pre-installed on a standard Linux
5. Python3


Clone the repo and follow the steps;


### Step 1: Train the ML model
- Install required dependencies and run the script `train.py`

    ```sh
        pip install -r requirements-ml.txt
        python3 train.py model_pipeline.joblib

    ```


### Step 2: Start minikube
- Clone this repo and execute the following command from its root:

    ```sh
    minikube start --driver=docker --mount --mount-string="${PWD}:/host" --ports=80:80,443:443
    ```
- Run the following to enable ingress API
    ```sh
    minikube addons enable ingress
    ```


### Step 3: Configure
- Setup requires some environment variables. See/edit the configuration section
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


### Step 4: Build docker images
- Run to build the backend and nginx docker images

    ```sh
    bash run.sh build

    ```


### Step 5: Run
- Run the following and wait for the kubernetes Deployment to complete

    ```sh
    bash run.sh run
    ```


Thats it! The app should be available at `http://localhost`



## How to run in production (prod mode)

In order to deploy to production, make sure the following resources are available;
1. A GKE cluster accessible through `kubectl`
2. A Google artifacts registry. Subsitute as __GOOGLE_ARTIFACTS_REG__
3. A GCS bucket for storing static files. Subsitute as __STATIC_FILES_GCS_BUCKET__
4. Set __RUN_MODE__ environment variable to `prod`


### Step 1: Build docker images
- `bash run.sh build`


### Step 2: Deploy
- `bash run.sh run`



Get nginx IP using;

```bash
    IP=$(kubectl get svc nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

Navigate to http://$IP

