from kiwi_berry.search import SearchParams

import datetime as dt


def test_search_from_url():
    search_params = SearchParams.from_url("https://api.tequila.kiwi.com/v2/search?fly_from=FRA&fly_to=PRG&date_from=01%2F10%2F2023&date_to=03%2F10%2F2023&return_from=04%2F10%2F2023&return_to=06%2F10%2F2023&nights_in_dst_from=2&nights_in_dst_to=3&max_fly_duration=20&ret_from_diff_city=true&ret_to_diff_city=true&one_for_city=0&one_per_date=0&adults=2&children=2&selected_cabins=C&mix_with_cabins=M&adult_hold_bag=1,0&adult_hand_bag=1,1&child_hold_bag=2,1&child_hand_bag=1,1&only_working_days=false&only_weekends=false&partner_market=us&max_stopovers=2&max_sector_stopovers=2&vehicle_type=aircraft&limit=500")

    assert search_params.model_dump() == {
            'adult_hand_bag': [1, 1],
            'adult_hold_bag': [1, 0],
            'adults': 2,
            'atime_from': None,
            'atime_to': None,
            'child_hand_bag': [1, 1],
            'child_hold_bag': [2, 1],
            'children': 2,
            'conn_on_diff_airport': None,
            'curr': None,
            'date_from': dt.date(2023, 10, 1),
            'date_to': dt.date(2023, 10, 3),
            'dtime_from': None,
            'dtime_to': None,
            'enable_vi': None,
            'fly_days': None,
            'fly_days_type': None,
            'fly_from': 'FRA',
            'fly_to': 'PRG',
            'infants': None,
            'limit': 500,
            'locale': None,
            'max_fly_duration': 20,
            'max_sector_stopovers': 2,
            'max_stopovers': 2,
            'mix_with_cabins': 'M',
            'nights_in_dst_from': 2,
            'nights_in_dst_to': 3,
            'one_for_city': False,
            'one_per_date': False,
            'only_weekends': False,
            'only_working_days': False,
            'partner_market': 'us',
            'price_from': None,
            'price_to': None,
            'ret_atime_from': None,
            'ret_atime_to': None,
            'ret_dtime_from': None,
            'ret_dtime_to': None,
            'ret_fly_days': None,
            'ret_fly_days_type': None,
            'ret_from_diff_airport': None,
            'ret_from_diff_city': True,
            'ret_to_diff_airport': None,
            'ret_to_diff_city': True,
            'return_from': dt.date(2023, 10, 4),
            'return_to': dt.date(2023, 10, 6),
            'select_airlines': None,
            'select_airlines_exclude': None,
            'select_stop_airport': None,
            'select_stop_airport_exclude': None,
            'selected_cabins': 'C',
            'sort': None,
            'stopover_from': None,
            'stopover_to': None,
            'vehicle_type': 'aircraft'
     }


def test_search_to_str_dict():
    search_params = SearchParams.from_url("https://api.tequila.kiwi.com/v2/search?fly_from=FRA&fly_to=PRG&date_from=01%2F10%2F2023&date_to=03%2F10%2F2023&return_from=04%2F10%2F2023&return_to=06%2F10%2F2023&nights_in_dst_from=2&nights_in_dst_to=3&max_fly_duration=20&ret_from_diff_city=true&ret_to_diff_city=true&one_for_city=0&one_per_date=0&adults=2&children=2&selected_cabins=C&mix_with_cabins=M&adult_hold_bag=1,0&adult_hand_bag=1,1&child_hold_bag=2,1&child_hand_bag=1,1&only_working_days=false&only_weekends=false&partner_market=us&max_stopovers=2&max_sector_stopovers=2&vehicle_type=aircraft&limit=500")

    dump = search_params.to_url_params()

    assert dump['adult_hand_bag'] == '1,1'
    assert dump['adult_hold_bag'] == '1,0'
    assert dump['adults'] == 2
    assert dump['child_hand_bag'] == '1,1'
    assert dump['child_hold_bag'] == '2,1'
    assert dump['children'] == 2
    assert dump['date_from'] == '01/10/2023'
    assert dump['date_to'] == '03/10/2023'
    assert dump['partner_market'] == 'us'


def test_search():
    search_params = SearchParams(
        fly_from='FRA',
        fly_to='CDG',
        date_from='2023-10-01',
        adults=1,
    )

    dump = search_params.to_url_params()
