import datetime as dt
import os
from logging import getLogger
from typing import Any, get_args, get_type_hints
from urllib import parse

import aiohttp
from pydantic import BaseModel, ConfigDict, computed_field, field_validator

from kiwi_berry.fucking_types import (
    CommaIntList,
    CommaStrList,
    IntBool,
    SlashDate,
    StrBool,
)

try:
    import orjson as json
except ImportError:
    import json  # type: ignore

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
    date_to: SlashDate | None = None

    adults: int
    children: int | None = None
    infants: int | None = None

    return_from: SlashDate | None = None
    return_to: SlashDate | None = None

    nights_in_dst_from: int | None = None
    nights_in_dst_to: int | None = None

    max_fly_duration: int | None = None

    ret_from_diff_city: StrBool | None = None
    ret_to_diff_city: StrBool | None = None

    one_for_city: IntBool | None = None
    one_per_date: IntBool | None = None

    selected_cabins: str | None = None
    mix_with_cabins: str | None = None

    adult_hold_bag: CommaIntList | None = None
    adult_hand_bag: CommaIntList | None = None

    child_hold_bag: CommaIntList | None = None
    child_hand_bag: CommaIntList | None = None

    fly_days: list | None = None
    fly_days_type: str | None = None

    ret_fly_days: list | None = None
    ret_fly_days_type: str | None = None

    only_working_days: StrBool | None = None
    only_weekends: StrBool | None = None

    partner_market: str | None = None

    curr: str | None = None
    locale: str | None = None

    price_from: int | None = None
    price_to: int | None = None

    dtime_from: dt.time | None = None
    dtime_to: dt.time | None = None
    atime_from: dt.time | None = None
    atime_to: dt.time | None = None

    ret_dtime_from: SlashDate | None = None
    ret_dtime_to: SlashDate | None = None
    ret_atime_from: SlashDate | None = None
    ret_atime_to: SlashDate | None = None

    stopover_from: dt.timedelta | None = None
    stopover_to: dt.timedelta | None = None

    max_stopovers: int | None = None
    max_sector_stopovers: int | None = None

    # https://tequila.kiwi.com/portal/docs/faq/itineraries_with_connection_on_different_airport
    conn_on_diff_airport: IntBool | None = None
    ret_from_diff_airport: IntBool | None = None
    ret_to_diff_airport: IntBool | None = None

    select_airlines: CommaStrList | None = None
    select_airlines_exclude: CommaStrList | None = None

    # stopover airport whitelist, blacklist
    select_stop_airport: CommaStrList | None = None
    select_stop_airport_exclude: CommaStrList | None = None

    vehicle_type: str | None = None
    enable_vi: IntBool | None = None
    sort: str | None = None
    limit: int | None = None

    @staticmethod
    def url_parse_type(value, typ):
        args = get_args(typ)
        if args:
            # Type is wrapped in Optional[...]
            typ = args[0]

        if typ == SlashDate:
            return dt.datetime.strptime(value, "%d/%m/%Y").date()

        if typ == CommaIntList:
            return [int(e) for e in value.split(",")]

        if typ == CommaStrList:
            return value.split(",")

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

        if typ == SlashDate:
            return value.strftime("%d/%m/%Y")

        if typ == CommaIntList:
            return ",".join(str(e) for e in value)

        if typ == CommaStrList:
            return ",".join(value)

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

        query = parse.urlparse(url).query
        query_qs = dict(parse.parse_qs(query).items())

        for k, v in query_qs.items():
            if len(v) > 1:
                log.warning("Multiple '%s' params in url", k)

        new_args = {}

        for arg, typ in get_type_hints(cls).items():
            if arg not in query_qs:
                continue

            value = query_qs[arg][0]
            value = cls.url_parse_type(value, typ)

            new_args[arg] = value

        return SearchParams(**new_args)

    def to_url_params(self) -> dict["str", Any]:
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
    equipment: str | None  # deprecated in favor of vehicle_type
    fare_basis: str
    fare_category: str
    fare_classes: str
    fare_family: str
    flight_no: str
    flyFrom: str
    flyTo: str
    guarantee: bool
    local_arrival: dt.datetime
    local_departure: dt.datetime
    operating_carrier: str
    operating_flight_no: str
    # return: IntBool  # return is a reserved word, so we parse this later
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

    @field_validator("flight_no", mode="before")
    def flight_no_str(cls, v):
        return str(v)

    def _repr_pretty_(self, cycle=False):
        return (
            f"\\ {self.local_departure:%Y-%m-%d} "
            f"{self.flyFrom}-{self.flyTo} {self.local_departure:%H:%M} "
            f"\\ {self.operating_carrier} {self.flight_no}"
        )


class Leg(BaseModel):
    sectors: list[Sector]
    return_leg: bool = False

    def _repr_pretty_(self, cycle=False):
        lines = []

        for i, sec in enumerate(self.sectors, 1):
            offset = i * " "
            lines.append(offset + sec._repr_pretty_())

        return "\n".join(lines)


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
    nightsInDest: int | None
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

    @property
    @computed_field
    def legs(self):
        outbound_sectors = []
        inbound_sectors = []

        for sector in self.route:
            if sector.return_leg is False:
                outbound_sectors.append(sector)
            else:
                inbound_sectors.append(sector)
        legs = [Leg(sectors=outbound_sectors)]
        if inbound_sectors:
            legs.append(Leg(sectors=inbound_sectors, return_leg=True))

        return legs

    def _repr_pretty_(self, cycle=False):
        secs = []
        secs.append(f"+---- {self.price} ----")
        for i, sec in enumerate(self.route, 1):
            offset = i * " "
            secs.append(offset + sec._repr_pretty_())
        return "\n".join(secs)


class Response(BaseModel):
    data: list[Itinerary]
    search_id: str
    currency: str
    fx_rate: float
    search_params: SearchParams | None = None

    @classmethod
    def from_json(cls, payload: bytes):
        data = json.loads(payload)

        return Response(**data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def show(self):
        return print("\n\n".join(i._repr_pretty_() for i in self.data))


class Client:
    server = "https://api.tequila.kiwi.com/v2"
    endpoint = "/search"

    def __init__(self, apikey=None):
        apikey = apikey or os.environ.get("KIWI_APIKEY")

        if not apikey:
            log.warning("No API key. Pass it to client as apikey arg," "or provide it as the KIWI_APIKEY env variable.")
        else:
            self.headers = {"apikey": apikey}

    async def search(self, search_params) -> Response:
        async with aiohttp.ClientSession(
            headers=self.headers,
            read_timeout=300,
        ) as sess, sess.get(self.server + self.endpoint, params=search_params.to_url_params()) as resp:
                if resp.status != 200:
                    log.error(f"{resp.url}\nHTTP Error {resp.status}: {await resp.text()}")
                    resp.raise_for_status()

                payload = await resp.read()

        response = Response.from_json(payload)
        if len(response) < 0:
            log.warning("Response had no results")
        return response


if __name__ == "__main__":
    import doctest

    doctest.testmod()
