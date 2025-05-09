"""
WSGI config for ml_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ml_server.settings')

application = get_wsgi_application()

from ml_api.registry import Registry
from ml_api.predict import CreateLogisticRegression

try:
    registry = Registry()
    lr = CreateLogisticRegression()
    registry.add_algorithm(endpoint_name="lor",
                            algorithm_object=lr,
                            algorithm_name="Logistic Regression",
                            algorithm_version="0.0.1",
                           )

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))



