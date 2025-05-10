import joblib
import pandas as pd
import os

from django.conf import settings

ARTIFACTS_DIR = str(os.path.join(settings.BASE_DIR) + "/artifacts")
LABELS = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}


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

        return {
            "prediction": prediction[0], 
            "prediction_label": LABELS[prediction[0]]
        }



    
