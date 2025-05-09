from rest_framework import serializers
from ml_api.models import Endpoint, Algorithm, Request


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "created_at")
        fields = read_only_fields


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        read_only_fields = ("id", "name", "version", "created_at", "endpoint")
        fields = read_only_fields


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        read_only_fields = ("id", "input_data", "response", "created_at", "algorithm")
        fields = ("id", "input_data", "response", "json_response", "feedback",
                  "created_at", "algorithm")
