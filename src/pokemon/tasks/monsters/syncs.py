from pokemon.celery import celery_app
from pokemon.domain.creatures import species
from pokemon.interfaces.api.monsters import serialisers
from pokemon.services import exceptions as json_client_exception, json_client
from pokemon.tools import loggers, urls

__all__ = [
    'update_creature',
]


@celery_app.task(
    autoretry_for=(
            json_client_exception.TooManyRequests,
            json_client_exception.UnableToConnect
    ),
    retry_kwargs={'max_retries': 2},
    retry_backoff=True,
    retry_backoff_max=5,
    retry_jitter=True,
)
def update_creature(
        *,
        limit: int,
        offset: int,
        **kwargs
) -> None:
    # Get each subset (with size 1) of total creature.
    # This is more robust than iterating through IDs as we do not know if
    # they recycle IDs or not.

    payload = json_client.pokemon_client.get_creature_subset(
        offset=offset, limit=limit)

    vendor_id = urls.get_vendor_id_from_url(url=payload['results'][0]['url'])

    creature_payload = json_client.pokemon_client.get_creature(
        vendor_id=vendor_id)

    species_description_payload = (
        json_client.pokemon_client.get_species_description(
            name=creature_payload['name'])
    )

    ability = serialisers.AbilityList(data=creature_payload['abilities'])
    species_description = serialisers.Description(
        data=species_description_payload)

    if any([not ability.is_valid(), not species_description.is_valid()]):
        # Just being slightly defensive. Log an error to Sentry when data
        # doesn't look sane
        loggers.celery.error(
            msg=f'Invalid payload received for creature - {vendor_id}')
        return

    species.sync(
        name=creature_payload['name'],
        vendor_id=creature_payload['id'],
        abilities=ability.data['ability'],
        color=species_description.validated_data['color'],
        shape=species_description.validated_data['shape'],
        is_baby=species_description.validated_data['is_baby'],
        is_legendary=species_description.validated_data['is_legendary'],
        is_mythical=species_description.validated_data['is_mythical'],
        forms_switchable=species_description.validated_data[
            'forms_switchable'],
        gender_rate=species_description.validated_data['gender_rate'],
    )
