import factory
from faker import Factory

from pokemon.data.monsters import models

__all__ = [
    'Creature',
    'Ability',
    'Description',
]

faker = Factory.create()


class Creature(factory.django.DjangoModelFactory):
    name = 'bulbasaur'
    vendor_id = 1

    class Meta:
        model = models.Creature


class Ability(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: faker.name())
    creature = factory.SubFactory(Creature)
    url = factory.lazy_attribute(lambda o: faker.uri())

    class Meta:
        model = models.Ability


class Description(factory.django.DjangoModelFactory):
    creature = factory.SubFactory(Creature)
    color = 'lue'
    shape = 'quadruped'
    is_baby = False
    is_legendary = False
    is_mythical = False
    forms_switchable = False
    gender_rate = 1

    class Meta:
        model = models.Description
