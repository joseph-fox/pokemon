from rest_framework import serializers


class Ability(serializers.Serializer):
    name = serializers.CharField(max_length=1000)
    url = serializers.URLField(max_length=2000)


class AbilityList(serializers.Serializer):
    ability = Ability(many=True)

    def __init__(self, data, *args, **kwargs):
        # This is untidy. Leave it as a discussion for next stage.
        _data = {
            'ability':
                [
                    {
                        'name': data_entry['ability']['name'],
                        'url': data_entry['ability']['url'],
                    }
                    for data_entry in data
                ]
        }

        super().__init__(data=_data, **kwargs)


class Description(serializers.Serializer):
    # Deliberately avoid using model serialiser there.
    color = serializers.CharField(max_length=500, source='color.name')
    shape = serializers.CharField(max_length=500, source='shape.name')
    is_baby = serializers.BooleanField()
    is_legendary = serializers.BooleanField()
    is_mythical = serializers.BooleanField()
    forms_switchable = serializers.BooleanField()
    gender_rate = serializers.IntegerField()

    def __init__(self, data, *args, **kwargs):
        _data = data.copy()

        # Flat out the nested data.
        # Untidy.
        _data['color'] = data['color']['name']
        _data['shape'] = data['shape']['name']

        super().__init__(data=_data, **kwargs)


class CreaturePayload(serializers.Serializer):
    id = serializers.IntegerField()
    vendor_id = serializers.IntegerField()
    name = serializers.CharField()
    abilities = Ability(many=True)
    color = serializers.CharField(source='description.color')
    shape = serializers.CharField(source='description.shape')
    is_baby = serializers.BooleanField(source='description.is_baby')
    is_legendary = serializers.BooleanField(source='description.is_legendary')
    is_mythical = serializers.BooleanField(source='description.is_mythical')
    forms_switchable = serializers.BooleanField(
        source='description.forms_switchable')
    gender_rate = serializers.IntegerField(source='description.gender_rate')
