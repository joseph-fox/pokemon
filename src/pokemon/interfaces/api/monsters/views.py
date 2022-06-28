from rest_framework import generics
from rest_framework import permissions

from pokemon.domain.creatures import species
from pokemon.interfaces.api.monsters import serialisers


class MonsterCatalogue(generics.ListAPIView):
    serializer_class = serialisers.CreaturePayload
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return species.get_species_with_description()
