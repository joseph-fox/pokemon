from django import shortcuts
from rest_framework import status

from tests import required_db

pytestmark = required_db


class TestCreatureQuery:

    def test_get_creatures_with_detail(self, anonymous_client, factory):
        description = factory.Description()
        factory.Ability(creature=description.creature)

        response = anonymous_client.get(
            path=shortcuts.reverse('api:monsters:monster-catalogue')
        )

        assert response.status_code == status.HTTP_200_OK
        payload = response.json()
        assert len(payload['results']) == 1
