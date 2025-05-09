from .models import Endpoint, Algorithm

class Registry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name, algorithm_version):
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name)

        database_object, algorithm_created = Algorithm.objects.get_or_create(
                name=algorithm_name,
                version=algorithm_version,
                endpoint=endpoint)

        self.endpoints[database_object.id] = algorithm_object




