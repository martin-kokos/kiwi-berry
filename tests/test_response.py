import json

from kiwi_berry.search import Response


def test_response(datadir):

    with open(datadir / "payload.json") as f:
        payload = json.loads(f.read())

    resp = Response(json=payload)
    assert len(resp) == 90
