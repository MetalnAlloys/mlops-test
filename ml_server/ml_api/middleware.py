import uuid

class SetRequestIdMiddleware:
    """
    Set a unique UUID for all incoming requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["uuid"] = uuid.uuid4()
        return self.get_response(request)
