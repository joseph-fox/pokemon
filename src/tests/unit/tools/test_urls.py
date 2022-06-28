from pokemon.tools import urls


class TestUrl:

    def test_get_vendor_id_from_url(self):
        expected_vendor_id = '1'
        url = f'https://pokeapi.co/api/v2/pokemon/{expected_vendor_id}/'

        vendor_id = urls.get_vendor_id_from_url(url=url)

        assert vendor_id == expected_vendor_id
