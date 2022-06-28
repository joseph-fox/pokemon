import pytest

required_db = pytest.mark.django_db(transaction=True)
