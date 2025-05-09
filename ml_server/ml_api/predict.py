import joblib
import pandas as pd
import os

from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
target_names = iris.target_names  # ['setosa' 'versicolor' 'virginica']


class CreateLogisticRegression:
    def __init__(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pipeline = joblib.load(os.path.join(root, "artifacts", "model_pipeline.joblib"))

    def preprocessing(self, input_data):
        data_array = pd.DataFrame(input_data, index=[0]).to_numpy()
        return pd.DataFrame(data_array, columns=iris.feature_names)

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)  
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

    def predict(self, input_data):
        prediction = self.pipeline.predict(input_data)[0]

        return {
            "prediction": prediction, 
            "prediction_label": target_names[prediction]
        }



    
