import sys, os
import joblib
import pandas as pd
import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


ARTIFACTS_DIR = os.environ.get("ARTIFACTS_DIR", "./ml_server/artifacts")

def main():
    if len(sys.argv) != 3 or sys.argv[1] == "--help":
        print("""
Usage: 
    python3 {} <input csv> <output filename> 
    e.g. python3 train.py data/iris.csv model_pipeline.joblib

Note: 
    - All trained models are stored in ./ml_server/artifacts dir. Override
              using the environment variabe ARTIFACTS_DIR""" 
              .format(sys.argv[0]))
        sys.exit(1)

    dataset = pd.read_csv(str(sys.argv[1]))

    X = dataset.iloc[:, [0,1,2, 3]].values
    y = dataset.iloc[:, 4].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression())
    ])

    pipeline.fit(X_train, y_train)

    output_file = sys.argv[2]
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR)
    
    print("[+] Saving trained model")
    joblib.dump(pipeline, os.path.join(ARTIFACTS_DIR, output_file))


if __name__ == "__main__":
    main()
