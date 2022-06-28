import mock

from pokemon.services import json_client


class TestJsonClient:

    # Mock the base client, so it won't hit the actual endpoint
    @mock.patch.object(json_client.BaseClient, 'get')
    def test_pokemon_client(self, get_method):
        # Get the Pokemon client
        client = json_client.PokemonClient()

        # Call the get_creature method
        _response = client.get_creatures()

        # Assertions
        get_method.assert_called_once()
