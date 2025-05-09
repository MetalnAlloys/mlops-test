import json

from rest_framework import viewsets, mixins, views, status
from rest_framework.response import Response

from ml_api.models import Endpoint, Algorithm, Request
from ml_api.serializers import AlgorithmSerializer, EndpointSerializer, RequestSerializer
from ml_server.wsgi import registry



class EndpointViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class AlgorithmViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AlgorithmSerializer
    queryset = Algorithm.objects.all()


class RequestViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()



class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        # Fetch and set the algorithm version from URI params 
        algorithm_version = self.request.query_params.get("version")
        algs = Algorithm.objects.filter(endpoint__name = endpoint_name)
        if algorithm_version is not None:
            algs = algs.filter(version = algorithm_version)

        if len(algs) == 0:
            return Response({"status": "Error", "message": "ML algorithm is not available"}, status=status.HTTP_400_BAD_REQUEST)

        algorithm_object = registry.endpoints[algs[0].id]

        prediction = algorithm_object.compute_prediction(request.data)

        label = prediction["prediction_label"] if "prediction_label" in prediction else "error"

        ml_request = Request(
            input_data=json.dumps(request.data),
            response=prediction,
            json_response=label,
            feedback="",
            algorithm=algs[0],
        )
        ml_request.save()

        # prediction["request_id"] = ml_request.id
        # Set unique request ID 
        prediction["request_id"] = request.META.get('uuid')
        prediction["model_version"] = algorithm_version
        print(request.META.get('uuid'))

        return Response(prediction)


