from django.db import transaction

from pokemon.data.monsters import models


# This function should not be here. Leave it here to save time.
# And, discuss it during the next stage.
@transaction.atomic(durable=True)
def sync(
        *,
        name: str,
        vendor_id: int,
        abilities: list,
        color: str,
        shape: str,
        is_baby: bool,
        is_legendary: bool,
        is_mythical: bool,
        forms_switchable: bool,
        gender_rate: bool,
):
    # Lock it
    creature, _ = models.Creature.objects.select_for_update().get_or_create(
        name=name,
        vendor_id=vendor_id,
    )

    for ability in abilities:
        creature.abilities.update_or_create(
            name=ability['name'],
            defaults={'url': ability['url']}
        )

    if creature.has_description():
        description_id = creature.description.id

        # Let us do a bulk update
        creature.description.__class__.objects.filter(
            id=description_id).update(
            color=color,
            shape=shape,
            is_baby=is_baby,
            is_legendary=is_legendary,
            is_mythical=is_mythical,
            forms_switchable=forms_switchable,
            gender_rate=gender_rate
        )
    else:
        models.Description.objects.create(
            creature=creature,
            color=color,
            shape=shape,
            is_baby=is_baby,
            is_legendary=is_legendary,
            is_mythical=is_mythical,
            forms_switchable=forms_switchable,
            gender_rate=gender_rate
        )


def get_species_with_description():
    return models.Creature.objects.exclude(
        description__isnull=True).order_by('id')
