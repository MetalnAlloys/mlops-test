#!/bin/bash

# impersonate a GCP service account to access cloud APIs

KSA=$1
GCLOUD_PROJECT_ID=$GCLOUD_PROJECT_ID
NAMESPACE=$NAMESPACE
ISA="{$2}@${GCLOUD_PROJECT_ID}.iam.gserviceaccount.com"


gcloud iam service-accounts add-iam-policy-binding $ISA \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:${GCLOUD_PROJECT_ID}.svc.id.goog[${NAMESPACE}/${KSA}]"

kubectl annotate serviceaccount $KSA iam.gke.io/gcp-service-account=$ISA
