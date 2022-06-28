from pokemon.services import exceptions as json_client_exceptions
from pokemon.services import json_client
from pokemon.tasks.monsters import syncs
from pokemon.tools import loggers


# Leave the Exception in the same module,
# so caller's life will be easier.
class UnableToFetchCreature(Exception):
    pass


def update_creatures(*, max_task_num: int = None):
    try:
        response = json_client.pokemon_client.get_creatures()
    except (
            json_client_exceptions.InvalidStatus,
            json_client_exceptions.UnableToConnect,
            json_client_exceptions.TooManyRequests,
    ):
        # Log it to Sentry to get the engineering attention
        # No need to add str(e) as Sentry will pick it automatically
        loggers.app_logger.exception(
            'Crawler is unable to fetch creature data')

        raise UnableToFetchCreature

    creature_num = response['count']

    if creature_num <= 0:
        # Early return as there is no creature to crawl
        return

    if max_task_num:
        creature_num = max_task_num

    for counter in range(creature_num):
        # Delay each task for 10 seconds to avoid possible db deadlock if
        # a worker retries.
        syncs.update_creature.apply_async(
            kwargs={'offset': counter, 'limit': 1},
            countdown=10,
            expires=120,
            queue='critical_tasks',
        )
