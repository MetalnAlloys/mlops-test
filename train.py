from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Load dataset
X, y = load_iris(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create pipeline with preprocessing and model
pipeline = Pipeline([
('scaler', StandardScaler()),
('model', LogisticRegression())
])

# Train
pipeline.fit(X_train, y_train)

# Save pipeline (includes preprocessing and model)
joblib.dump(pipeline, './ml_server/artifacts/model_pipeline.joblib')
