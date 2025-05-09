import inspect
from .registry import Registry
from django.test import TestCase
from .predict import CreateLogisticRegression

class MLTests(TestCase):
    def test_algorithm(self):
        input_data = {
         'sepal_length': 5.1,
         'sepal_width': 3.5,
         'petal_length': 1.4,
         'petal_width': 0.2
        }

        alg = CreateLogisticRegression()
        response = alg.compute_prediction(input_data)
        self.assertTrue('prediction_label' in response)
        self.assertEqual('setosa', response['prediction_label'])


    def test_registry(self):
        registry = Registry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "lr"
        algorithm_object = CreateLogisticRegression()
        algorithm_name = "Logistic regression"
        algorithm_version = "0.0.1"

        # Test adding an algorithm to registry
        registry.add_algorithm(endpoint_name,
                               algorithm_object,
                               algorithm_name,
                               algorithm_version)
        self.assertEqual(len(registry.endpoints), 1)




