__all__ = [
    'get_creature_subset_payload',
    'get_species_description_payload',
    'get_creature_payload',
]


def get_creature_payload():
    return {
        "abilities": [
            {
                "ability": {
                    "name": "overgrow",
                    "url": "https://pokeapi.co/api/v2/ability/65/"
                },
            },
            {
                "ability": {
                    "name": "chlorophyll",
                    "url": "https://pokeapi.co/api/v2/ability/34/"
                },
            }
        ],

        "id": 1,
        "name": "bulbasaur",

    }


def get_creature_subset_payload():
    return {
        "results": [
            {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon/1/"
            }
        ]
    }


def get_species_description_payload():
    return {
        "color": {
            "name": "green",
            "url": "https://pokeapi.co/api/v2/pokemon-color/5/"
        },
        "forms_switchable": False,
        "gender_rate": 1,

        "is_baby": False,
        "is_legendary": False,
        "is_mythical": False,
        "shape": {
            "name": "quadruped",
            "url": "https://pokeapi.co/api/v2/pokemon-shape/8/"
        },
    }
