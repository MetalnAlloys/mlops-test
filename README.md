# mlops-test

MLOps example Pipeline setup 


## Pipeline architecture and design


### Worklow Cycle

Train ML Model → save to disk → serve as HTTP endpoint → predict


### Components

1. Web server
    - Django + DRF (Django Rest Framework) as a backend for serving predictions
    - REST API:
    - `/api/v1/endpoints` list available endpoints
    - `/api/v1/algorithms` list registered algorithms
    - `/api/v1/requests` list all the processed requests
    - `/api/v1/lor/predict` run a prediction. (_lor=logistic regression_)
    - `/grafana` for grafana GUI
    - `/prometheus` for prometheus Web UI
    - `/metrics` to list all the collected metrics


2. Proxy
    - Nginx as a reverse proxy for all microservices


3. Monitoring/Observability
    - Prometheus to collect metrics. See `ml_server/ml_api/predict.py` for example usage on defining custom metrics
    - Grafana to set up visual dashboards for metrics


4. Model Training
    - A sample Logistic Regression model trained on Python Scikit Iris database. Uses CSV based input


5. Database
    - Postgresql


6. CI/CD Pipeline (Untested)
    - `./github/workflows/ci-pr.yaml` to run unit tests, retrain model and test deployment


7. Kubernetes based deployment
    - Microservices based.
    - Services: backend, nginx, grafana, prometheus, postgres



## How to run locally (dev mode)

In order to run locally, the following binaries are required;

1. [minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
2. [kubectl](https://kubectl.docs.kubernetes.io/)
3. A running Docker daemon
4. It also requires a small tool called `envsubst` but it is assumed as
   pre-installed on a standard Linux
5. Python


Clone the repo and follow these steps;


### Step 1: Train the ML model
- Install required dependencies and run the script `train.py`
- Check `python3 train.py --help` for more info

    ```sh
        pip install -r requirements-ml.txt
        python3 train.py data/iris.csv model_pipeline.joblib

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
    + __PIPELINE:__ Path to the model artifact.


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


### Steo 6: Undeploy
- Run `bash run.sh stop` to delete deployment



## How to run in production (prod mode)

In order to deploy to production, make sure the following resources are available;
Note that this setup is created with GCP and GKE in mind.

1. A GKE cluster accessible through `kubectl`
2. A Google artifacts registry. Subsitute as __GOOGLE_ARTIFACTS_REG__
3. A GCS bucket for storing static files. Subsitute as __STATIC_FILES_GCS_BUCKET__
4. Set __RUN_MODE__ environment variable to `prod`
5. A GCP service account with at least the following roles:
    + `roles/container.viewer`
    + `roles/iam.serviceAccountTokenCreator`
    + `roles/storage.objectUser`   


### Step 1: Build docker images
- `bash run.sh build`


### Step 2: Deploy
- `bash run.sh run`


### Step 3: GCP related stuff
The backend and nginx require access to a GCS bucket which means they should have some permissions granted to them. There are multiple ways to do it, however in this case I have used Workload Identity Federation to impersonate a GCP service account. Note that every Kubernetes service in this project has a Kubernetes service account attached to it. We will let these service accounts impersonate a GCP service account.

- Use the script `impersonate_svc_account.sh` to do this
- Script usage: `bash impersonate_svc_account.sh <kubernetes service account name> <GCP service account name>`
        
   ```bash
     export NAMESPACE=kubernetes-namespace
     export GCLOUD_PROJECT_ID=my-gcloud-project-id
     bash impersonate_svc_account.sh backend gcp-service-account
   ```


Get nginx IP using;

```bash
    IP=$(kubectl get svc nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

Navigate to http://$IP


### Steo 2: Undeploy
- Run `bash run.sh stop` to delete deployment


## Usage
### Testing the default app
The deployed app can be tested both using a Browser and cli tools such as curl.

Prediction can be done using the endpoint: `/api/v1/lor/predict` 

It also takes a `version` URI parameter. Available versions for an algorithm can be found by calling the endpoint: `/api/v1/alogirithms`


e.g. test using curl
```bash
$ cat data.json
{
"sepal_length": 5.1,
"sepal_width": 1.0,
"petal_length": 1.2,
"petal_width": 0.2
}

$ curl --header "Content-Type: application/json" --request POST  --data @data.json  http://localhost/api/v1/lor/predict?version=0.0.1

```


You can also call these endpoints using your Browser by taking advantange of DRF (django rest framework) graphical interface. Just navigate to `http://localhost/api/v1/lor/predict?version=0.0.1` and type in the JSON payload. It is a quicker way to visualize all the other endpoints as well.

