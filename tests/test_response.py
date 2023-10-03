import json
from kiwi_berry.search import Response
from kiwi_berry.search import Itinerary
from kiwi_berry.search import Sector


def test_sector(shared_datadir):

    with open(shared_datadir / "search_response.json", "rb") as f:
        payload = f.read()
    data = json.loads(payload)
    sector_data = data['data'][0]['route'][0]
    s = Sector(**sector_data)
    assert s.flyFrom == 'FRA'


def test_itinerary(shared_datadir):

    with open(shared_datadir / "search_response.json", "rb") as f:
        payload = f.read()
    data = json.loads(payload)
    itinerary_data = data['data'][0]
    i = Itinerary(**itinerary_data)
    assert i.flyFrom == 'FRA'


def test_response(shared_datadir):

    with open(shared_datadir / "search_response.json", "rb") as f:
        payload = f.read()

    resp = Response.from_json(payload)

    assert resp[0].flyFrom == 'FRA'
    assert resp[1].price == 3622
    assert len(resp) == 90
