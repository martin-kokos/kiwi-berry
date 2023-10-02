from urllib import parse
from typing import Any, Optional, get_args, get_origin, get_type_hints, get_origin

import datetime as dt

from logging import getLogger

from pydantic import BaseModel, ConfigDict, field_validator

from kiwi_berry.fucking_types import CommaStrList, SlashDate
from kiwi_berry.fucking_types import IntBool
from kiwi_berry.fucking_types import CommaIntList

log = getLogger(__name__)


def url_serialize(value: bool | list | str) -> str:
    """Convert to kiwi-specific types

    >>> url_serialize([True, 'a'])
    '1,a'
    """
    if isinstance(value, bool):
        value = str(int(value))

    elif isinstance(value, list | tuple | set):
        value = ','.join(url_serialize(v) for v in value)

    return value


def url_deserialize(value: str) -> list[str] | str | bool:
    """Convert from kiwi-specific types

    >>> url_deserialize('CDG,STN')
    ['CDG', 'STN']
    """
    if ',' in value:
        value = value.split(',')

    return value


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

    return_from: Optional[SlashDate] = None
    return_to: Optional[SlashDate] = None

    nights_in_dst_from: Optional[int] = None
    nights_in_dst_to: Optional[int] = None

    max_fly_duration: Optional[int] = None

    ret_from_diff_city: bool = True
    ret_to_diff_city: bool = True

    one_for_city: IntBool = False
    one_per_date: IntBool = False

    adults: int = 1
    children: int = 0
    infants: int = 0

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

    only_working_days: bool = False
    only_weekends: bool = False

    partner_market: str | None = None

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
    conn_on_diff_airport: IntBool = True
    ret_from_diff_airport: IntBool = True
    ret_to_diff_airport: IntBool = True

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
    def get_field_type(f):
        args = get_args(f)
        if args:
            # Type is wrapped in Optional[...]
            return args[0]
        else:
            return f

    @classmethod
    def from_url(cls, url):
        """
        Convert url string for an API request to the SearchParams class
        with all the weird type conversions.
        """

        query = parse.urlparse(
            url
        ).query
        query_qs = parse.parse_qs(query)

        for k, v in query_qs.items():
            if len(v) > 1:
                log.warn("Multiple '%s' params in url", k)

        query_qs = {k: v[0] for k, v in query_qs.items()}

        for arg, typ in get_type_hints(cls).items():
            if arg not in query_qs:
                continue

            typ = cls.get_field_type(typ)

            if typ in (SlashDate, CommaIntList):
                query_qs[arg] = typ.from_url_fmt(query_qs[arg])

        return SearchParams(**query_qs)

    @field_validator('date_from', 'date_to')
    @classmethod
    def date_validator(cls, v: Any):
        if isinstance(v, str):
            v = SlashDate(*dt.datetime.strptime(v, "%Y-%m-%d").timetuple()[:3])
        return v

    def strig_dict(self):
        return None


class Client():

    server = 'https://api.tequila.kiwi.com/v2'
    endpoint = '/search'
    apikey = None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
