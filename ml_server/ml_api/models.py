from django.db import models

class Endpoint(models.Model):
    """
    List available endpoints

    Attributes:
        name: The name of the endpoint
    """
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Algorithm(models.Model):
    """
    Model to store information about the Algorithm.

    Attributes:
        name: The name of the algorithm.
        version: The version of the algorithm.
        endpoint: The Endpoint associated with the algorithm.
    """
    name = models.CharField(max_length=128)
    version = models.CharField(max_length=128)
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Request(models.Model):
    """
    Request storage for all the processed requests

    Attributes:
        input_data: The input data in JSON format.
        response: The response of the ML algorithm.
        json_response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        algorithm: The reference to MLAlgorithm used to compute response.
    """
    input_data = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    json_response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
