from aiohttp.client_exceptions import ClientResponseError
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.fields import Field
import aiohttp

from kiwi_berry.fucking_types import CommaStrList, SlashDate
from kiwi_berry.fucking_types import IntBool, StrBool
from kiwi_berry.fucking_types import CommaIntList

from typing import Any, Optional, get_args, get_type_hints

import datetime as dt

from logging import getLogger
from urllib import parse

import os

try:
    import orjson as json
except ImportError:
    import json

log = getLogger(__name__)


class SearchParams(BaseModel):
    """
    https://tequila.kiwi.com/portal/docs/tequila_api/search_api

    Yes, some bools are 0/1 some false/true.
    Yes, date is %d-%m-%Y.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    fly_from: str
    fly_to: str

    date_from: SlashDate
    date_to: SlashDate

    adults: int
    children: Optional[int] = None
    infants: Optional[int] = None

    return_from: Optional[SlashDate] = None
    return_to: Optional[SlashDate] = None

    nights_in_dst_from: Optional[int] = None
    nights_in_dst_to: Optional[int] = None

    max_fly_duration: Optional[int] = None

    ret_from_diff_city: Optional[StrBool] = None
    ret_to_diff_city: Optional[StrBool] = None

    one_for_city: Optional[IntBool] = None
    one_per_date: Optional[IntBool] = None

    selected_cabins: Optional[str] = None
    mix_with_cabins: Optional[str] = None

    adult_hold_bag: Optional[CommaIntList] = None
    adult_hand_bag: Optional[CommaIntList] = None

    child_hold_bag: Optional[CommaIntList] = None
    child_hand_bag: Optional[CommaIntList] = None

    fly_days: Optional[list] = None
    fly_days_type: Optional[str] = None

    ret_fly_days: Optional[list] = None
    ret_fly_days_type: Optional[str] = None

    only_working_days: Optional[StrBool] = None
    only_weekends: Optional[StrBool] = None

    partner_market: Optional[str] = None

    curr: Optional[str] = None
    locale: Optional[str] = None

    price_from: Optional[int] = None
    price_to: Optional[int] = None

    dtime_from: Optional[dt.time] = None
    dtime_to: Optional[dt.time] = None
    atime_from: Optional[dt.time] = None
    atime_to: Optional[dt.time] = None

    ret_dtime_from: Optional[SlashDate] = None
    ret_dtime_to: Optional[SlashDate] = None
    ret_atime_from: Optional[SlashDate] = None
    ret_atime_to: Optional[SlashDate] = None

    stopover_from: Optional[dt.timedelta] = None
    stopover_to: Optional[dt.timedelta] = None

    max_stopovers: Optional[int] = None
    max_sector_stopovers: Optional[int] = None

    # https://tequila.kiwi.com/portal/docs/faq/itineraries_with_connection_on_different_airport
    conn_on_diff_airport: Optional[IntBool] = None
    ret_from_diff_airport: Optional[IntBool] = None
    ret_to_diff_airport: Optional[IntBool] = None

    select_airlines: Optional[CommaStrList] = None
    select_airlines_exclude: Optional[CommaStrList] = None

    # stopover airport whitelist, blacklist
    select_stop_airport: Optional[CommaStrList] = None
    select_stop_airport_exclude: Optional[CommaStrList] = None

    vehicle_type: Optional[str] = None
    enable_vi: Optional[IntBool] = None
    sort: Optional[str] = None
    limit: Optional[int] = None

    @staticmethod
    def url_parse_type(value, typ):
        args = get_args(typ)
        if args:
            # Type is wrapped in Optional[...]
            typ = args[0]
        else:
            typ = typ

        if typ == SlashDate:
            return dt.datetime.strptime(value, '%d/%m/%Y').date()

        if typ == CommaIntList:
            return [int(e) for e in value.split(',')]

        if typ == CommaStrList:
            return value.split(',')

        if typ == IntBool:
            return bool(int(value))

        if typ == StrBool:
            return value  # pydantic can deal with lowercase bool

        return value

    @staticmethod
    def url_serialize_type(value, typ):
        args = get_args(typ)
        if args:
            # Type is wrapped in Optional[...]
            typ = args[0]
        else:
            typ = typ

        if typ == SlashDate:
            return value.strftime('%d/%m/%Y')

        if typ == CommaIntList:
            return ','.join(str(e) for e in value)

        if typ == CommaStrList:
            return ','.join(value)

        if typ == IntBool:
            return str(int(value))

        if typ == StrBool:
            return str(value).lower()

        return value

    @classmethod
    def from_url(cls, url):
        """
        Convert url string for an API request to the SearchParams class
        with all the weird type conversions.
        """

        query = parse.urlparse(
            url
        ).query
        query_qs = dict(parse.parse_qs(query).items())

        for k, v in query_qs.items():
            if len(v) > 1:
                log.warn("Multiple '%s' params in url", k)

        new_args = {}

        for arg, typ in get_type_hints(cls).items():
            if arg not in query_qs:
                continue

            value = query_qs[arg][0]
            value = cls.url_parse_type(value, typ)

            new_args[arg] = value

        return SearchParams(**new_args)

    def to_url_params(self) -> dict['str', Any]:
        """
        Convert to url params of which some types are oddly formated
        """
        model_dict = self.model_dump()

        new_dict = {}
        for arg, typ in get_type_hints(self).items():
            value = model_dict[arg]

            if value is None:
                continue

            value = self.url_serialize_type(value, typ)
            new_dict[arg] = value

        return new_dict


class Sector(BaseModel):

    id: str
    bags_recheck_required: bool
    cityCodeFrom: str
    cityCodeTo: str
    cityFrom: str
    cityTo: str
    combination_id: str
    equipment: Optional[str]  # deprecated in favor of vehicle_type
    fare_basis: str
    fare_category: str
    fare_classes: str
    fare_family: str
    flight_no: str
    flyFrom: str
    flyTo: str
    guarantee: bool
    id: str
    local_arrival: dt.datetime
    local_departure: dt.datetime
    operating_carrier: str
    operating_flight_no: str
    #return: IntBool  # return is a reserved word, so we have to add this later
    return_leg: IntBool
    utc_arrival: dt.datetime
    utc_departure: dt.datetime
    vehicle_type: str
    vi_connection: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **kwargs):
        # rename arg from reserved word "return"
        kwargs["return_leg"] = kwargs["return"]
        super().__init__(**kwargs)

    @field_validator('flight_no', mode='before')
    def flight_no_str(cls, v):
        return str(v)

    def ascii_render(self):
        return f'\\ {self.local_departure:%Y-%m-%d} {self.flyFrom}-{self.flyTo} {self.local_departure:%H:%M} \\ {self.operating_carrier} {self.flight_no}'


class Itinerary(BaseModel):

    airlines: list[str]
    availability: dict
    baglimit: dict
    bags_price: dict
    booking_token: str
    cityCodeFrom: str
    cityCodeTo: str
    cityFrom: str
    cityTo: str
    conversion: dict
    countryFrom: dict
    countryTo: dict
    deep_link: str
    distance: float
    duration: dict
    facilitated_booking_available: bool
    fare: dict
    flyFrom: str
    flyTo: str
    has_airport_change: bool
    hidden_city_ticketing: bool
    id: str
    local_arrival: dt.datetime
    local_departure: dt.datetime
    nightsInDest: Optional[int]
    pnr_count: int
    price: float
    quality: float
    route: list[Sector]
    technical_stops: int
    throw_away_ticketing: bool
    utc_arrival: dt.datetime
    utc_departure: dt.datetime
    virtual_interlining: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def ascii_render(self):
        secs = []
        secs.append(f'+---- {self.price} ----')
        for i, sec in enumerate(self.route, 1):
            offset = i * ' '
            secs.append(offset + sec.ascii_render())
        return '\n'.join(secs)


class Response(BaseModel):

    data: list[Itinerary]
    search_id: str
    currency: str
    fx_rate: float
    search_params: Optional[SearchParams] = None

    @classmethod
    def from_json(cls, payload: bytes):
        data = json.loads(payload)

        return Response(**data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def show(self):
        return print('\n\n'.join(i.ascii_render() for i in self.data))


class Client():

    server = 'https://api.tequila.kiwi.com/v2'
    endpoint = '/search'

    def __init__(self, apikey=None):

        apikey = apikey or os.environ.get('KIWI_APIKEY')

        if not apikey:
            log.warn('No API key. Pass it to client as apikey arg,'
                     'or provide it as the KIWI_APIKEY env variable.')
        else:
            self.headers = {
                'apikey': apikey
            }

    async def search(self, search_params) -> Response:
        async with aiohttp.ClientSession(
            headers=self.headers,
            read_timeout=300,
        ) as sess:
            async with sess.get(
                    self.server + self.endpoint,
                    params=search_params.to_url_params()
                    ) as resp:

                if resp.status != 200:
                    log.error(f"{resp.url}\nHTTP Error {resp.status}: {await resp.text()}")
                    resp.raise_for_status()

                payload = await resp.read()

        response = Response.from_json(payload)
        if len(response) < 0:
            log.warn('Response had no results')
        return response


if __name__ == "__main__":
    import doctest
    doctest.testmod()
