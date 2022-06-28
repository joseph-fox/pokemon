import mock

from pokemon.domain.creatures import crawlers


class TestCrawler:

    @mock.patch.object(crawlers.syncs, 'update_creature')
    @mock.patch.object(crawlers.json_client.pokemon_client, 'get_creatures')
    def test_fetch_creatures(self, get_creatures, update_creature):
        # Prepare factories
        get_creatures.return_value = {'count': 1}

        # Call the function
        crawlers.update_creatures()

        # Assertions
        get_creatures.assert_called_once()
        update_creature.apply_async.assert_called_once()
