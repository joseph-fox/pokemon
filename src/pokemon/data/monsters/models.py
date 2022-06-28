from django.core import exceptions as django_exceptions
from django.db import models


class Creature(models.Model):
    vendor_id = models.IntegerField(help_text='ID from source vendor')
    name = models.CharField(max_length=500)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vendor_id', 'name'],
                name='unique_vendor_identifier')
        ]

        indexes = [
            models.Index(
                fields=['vendor_id', 'name']
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} - ID: {self.id}"

    def has_description(self) -> bool:
        # This is not a property because it hits db.
        try:
            return bool(self.description)
        except django_exceptions.ObjectDoesNotExist:
            return False


class Ability(models.Model):
    name = models.CharField(max_length=1000)
    creature = models.ForeignKey(
        Creature, related_name='abilities', on_delete=models.PROTECT)
    url = models.URLField(max_length=2000)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'An ability for creature {self.creature.id}'


class Description(models.Model):
    # I am not familiar with the Pokemon game.
    # Usually, I'd ask Pokemon gurus from the team for more info.
    # But, this is a test to be done within hours.
    # So, I create the description basing on my own understanding.
    # Leave this as a discussion for the next stage.
    creature = models.OneToOneField(
        Creature,
        related_name='description',
        on_delete=models.PROTECT,
    )
    color = models.CharField(max_length=500)
    shape = models.CharField(max_length=500)

    is_baby = models.BooleanField()
    is_legendary = models.BooleanField()
    is_mythical = models.BooleanField()
    forms_switchable = models.BooleanField()
    gender_rate = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Description for creature - {self.creature.id}'
