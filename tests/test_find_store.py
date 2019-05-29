import pytest
from app.find_store import *

stores_list = list(DictReader(open("store-locations.csv")))

def test_load_stores_list():
    expected = {}
    expected['Store Name'] = 'Crystal'
    expected['Store Location'] = 'SWC Broadway & Bass Lake Rd'
    expected['Address'] = '5537 W Broadway Ave'
    expected['City'] = 'Crystal'
    expected['State'] = 'MN'
    expected['Zip Code'] = '55428-3507'
    expected['Latitude'] = '45.0521539'
    expected['Longitude'] = '-93.364854'
    expected['County'] = 'Hennepin County'

    stores_list = load_stores_list()
    assert stores_list[0] == expected

def test_get_start_loc_geocode_with_zip():
    expected = {
        "lat": 35.273127,
        "lng": -120.721971
    }

    start_loc_geocode = get_start_loc_geocode('93405')
    assert start_loc_geocode == expected

def test_get_start_loc_geocode_with_address():
    expected = {
        "lat": 37.793819,
        "lng": -122.395089
    }

    start_loc_geocode = get_start_loc_geocode('1 Market St San Francisco CA')
    assert start_loc_geocode == expected

def test_find_closest_store_idx():
    expected_closest_store_idx = 0

    closest_store = find_closest_store({"lat": 45.0521539, "lng": -93.364854}, 'mi', stores_list)
    assert closest_store['idx'] == expected_closest_store_idx

def test_find_closest_store_store_name():
    expected_closest_store_name = 'Yakima'

    closest_store = find_closest_store({"lat": 46.606832, "lng": -120.488248}, 'mi', stores_list)
    assert stores_list[closest_store['idx']]['Store Name'] == expected_closest_store_name



