from django.test import TestCase

from .registry import Registry
from .predict import CreateLogisticRegression

class MLOpsTests(TestCase):
    def test_logistic_regression_algorithm(self):
        input_data = {
         'sepal_length': 5.1,
         'sepal_width': 3.5,
         'petal_length': 1.4,
         'petal_width': 0.2
        }

        test_algorithm = CreateLogisticRegression()
        response = test_algorithm.compute_prediction(input_data)
        self.assertTrue('prediction_label' in response)
        self.assertEqual('setosa', response['prediction_label'])


    def test_adding_new_algorithm(self):
        registry = Registry()
        self.assertEqual(len(registry.endpoints), 0)

        endpoint_name = "lar"
        algorithm_object = CreateLogisticRegression()
        algorithm_name = "Logistic regression"
        algorithm_version = "0.0.1"

        # Test adding an algorithm to the registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name, algorithm_version)
        self.assertEqual(len(registry.endpoints), 1)




