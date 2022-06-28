import mock
from django.core.management import call_command

from tests import required_db

pytestmark = required_db


class TestSyncCreature:
    """
    Test every engineering components required for update creatures.
    """

    @mock.patch('pokemon.services.json_client.pokemon_client', autospec=True)
    def test_update_creature_description(self, pokeman_client, factory):
        # Create a fixture in db.
        creature = factory.Creature()

        # Mock API calls
        pokeman_client.get_creatures.return_value = {"count": 1}

        pokeman_client.get_creature.return_value = (
            factory.get_creature_payload())

        pokeman_client.get_creature_subset.return_value = (
            factory.get_creature_subset_payload())

        pokeman_client.get_species_description.return_value = (
            factory.get_species_description_payload())

        # Confirm no description before running the management command
        assert not creature.has_description()

        # Call the management command
        call_command('sync_pokemon')

        # Assertions
        creature.refresh_from_db()

        assert creature.has_description()
        assert creature.abilities.count() == 2
