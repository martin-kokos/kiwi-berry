from kiwi_berry.search import SearchParams


def test_search_from_url():
    search_params = SearchParams.from_url("https://api.tequila.kiwi.com/v2/search?fly_from=FRA&fly_to=PRG&date_from=01%2F10%2F2023&date_to=03%2F10%2F2023&return_from=04%2F10%2F2023&return_to=06%2F10%2F2023&nights_in_dst_from=2&nights_in_dst_to=3&max_fly_duration=20&ret_from_diff_city=true&ret_to_diff_city=true&one_for_city=0&one_per_date=0&adults=2&children=2&selected_cabins=C&mix_with_cabins=M&adult_hold_bag=1,0&adult_hand_bag=1,1&child_hold_bag=2,1&child_hand_bag=1,1&only_working_days=false&only_weekends=false&partner_market=us&max_stopovers=2&max_sector_stopovers=2&vehicle_type=aircraft&limit=500")

    print(search_params.strig_dict())


def test_search_to_url():
    search_params = SearchParams(**{
        'fly_from': "CDG",
        'fly_to': "JFK",
        'date_from': '2023-12-12',
        'date_to': '2023-12-12',
        'return_from': '2023-12-22',
        'return_to': '2023-12-22',
        })

    print(search_params.strig_dict())
