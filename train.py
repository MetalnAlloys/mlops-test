import sys, os
import joblib
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


ARTIFACTS_DIR = os.environ.get("ARTIFACTS_DIR", "./ml_server/artifacts")

def main():
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        print("""
Usage: 
    python3 {} <output filename> 
    e.g. python3 train.py model_pipeline.joblib

Note: 
    - All trained models are stored in ./ml_server/artifacts dir """ .format(sys.argv[0]))
        sys.exit(1)

    # Load Iris dataset
    X, y = load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Create pipeline with preprocessing and model
    pipeline = Pipeline([('scaler', StandardScaler()),('model', LogisticRegression())])
    pipeline.fit(X_train, y_train)

    output_file = sys.argv[1]
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR)
    
    print("[+] Saving trained model")
    joblib.dump(pipeline, os.path.join(ARTIFACTS_DIR, output_file))


if __name__ == "__main__":
    main()
