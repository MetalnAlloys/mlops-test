import joblib
import pandas as pd
import os
import time

from django.conf import settings

from prometheus_client import Counter, Histogram, generate_latest

ARTIFACTS_DIR = str(os.path.join(settings.BASE_DIR) + "/artifacts")
LABELS = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}

# Prometheus metrics
REQUEST_COUNT = Counter('model_requests_total', 'Total number of prediction requests')
REQUEST_LATENCY = Histogram('model_request_latency_seconds', 'Latency of prediction requests')
PREDICTION_CONFIDENCE = Histogram('model_prediction_confidence', 'Confidence of positive class prediction')

class CreateLogisticRegression:
    def __init__(self):
        self.pipeline = joblib.load(os.path.join(ARTIFACTS_DIR, "model_pipeline.joblib"))

    def preprocessing(self, input_data):
        return pd.DataFrame(input_data, index=[0]).to_numpy()

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)  
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

    def predict(self, input_data):
        prediction = self.pipeline.predict(input_data)

        start_time = time.time()
        REQUEST_COUNT.inc()
        PREDICTION_CONFIDENCE.observe(prediction[0])
        REQUEST_LATENCY.observe(time.time() - start_time)

        return {
            "prediction": prediction[0], 
            "prediction_label": LABELS[prediction[0]]
        }



    
