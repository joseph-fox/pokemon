import pytest
from django.test import client

from . import factories


@pytest.fixture
def anonymous_client():
    """
    A Django test client without auth credentials
    """
    return client.Client()


@pytest.fixture
def factory():
    return factories
