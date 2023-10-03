from kiwi_berry.search import SearchParams, Client

import asyncio

query = SearchParams(
    fly_from='FRA',
    fly_to='HKT',
    date_from='2023-11-20',
    date_to='2023-11-30',
    adults=1,
    limit=10,
    sort='price'
)
resp = asyncio.run(Client().search(query))
resp.show()
