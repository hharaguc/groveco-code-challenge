"""

Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>            Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address="<address>"  Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)        Display units in miles or kilometers [default: mi]
  --output=(text|json)   Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km

"""

from docopt import docopt
from docopt import __version__ as VERSION
from csv import DictReader
from math import cos, asin, sqrt
import requests
import json

# Using the MapQuest Geocoding API to geocode the zip code and address arguments
# Geocoding API documentation: https://developer.mapquest.com/documentation/geocoding-api/address/get/
# Geocoding API sandbox: https://developer.mapquest.com/documentation/samples/geocoding/v1/address/ 
api_key = json.loads(open("mapquest_api_key.json").read())["api_key"]
mapquest_geocode_endpt = 'http://www.mapquestapi.com/geocoding/v1/address?key=' + api_key + '&location='

# Reads the .csv file of stores
def load_stores_list():
    return list(DictReader(open("store-locations.csv")))

# Gets the geocode of the starting location
def get_start_loc_geocode(start_loc):
    try:
        response = requests.get(mapquest_geocode_endpt + start_loc)
        response.raise_for_status()
        response_content = json.loads(response.content.decode('utf-8'))
        start_lat_lng = response_content['results'][0]['locations'][0]['displayLatLng']
        return start_lat_lng
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

# Calculates the distance between two points using the Haversine formula
# Reference: https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude
def calc_distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

# Calculates the distance from the starting point to each store
# Returns the index of the nearest store and the distance away (in the specified |units|)
def find_closest_store(start_lat_lng, units, output, stores_list):
    KM_TO_MI = .621371

    distances = {}
    start_lat = start_lat_lng['lat']
    start_lng = start_lat_lng['lng']

    for idx, store in enumerate(stores_list):
        end_lat = float(store['Latitude'])
        end_lng = float(store['Longitude'])

        distances[idx] = calc_distance(start_lat, start_lng, end_lat, end_lng)

    closest_store = {}
    closest_store['idx'] = min(distances, key=distances.get)

    if units == 'km':
        closest_store['distance_away'] = distances[closest_store['idx']]
    else: # units == 'mi'
        closest_store['distance_away'] = distances[closest_store['idx']] * KM_TO_MI

    return closest_store

if __name__ == '__main__':
    expected_units = ['mi', 'km']
    expected_outputs = ['text', 'json']

    # Parse and validate command line arguments
    args = docopt(__doc__, version=VERSION)
    start_loc = args['--address'] if args['--address'] else args['--zip']
    units = args['--units']
    output = args['--output']

    if units not in expected_units:
        exit(units + ' is not a valid --unit argument.' + __doc__)
    if output not in expected_outputs:
        exit(output + ' is not a valid --output argument.' + __doc__)

    # Find the closest store
    stores_list = load_stores_list()
    start_lat_lng = get_start_loc_geocode(start_loc)
    closest_store = find_closest_store(start_lat_lng, units, output, stores_list)
    
    # Print the results!
    store_details = stores_list[closest_store['idx']]
    store_details['Distance Away'] = closest_store['distance_away']

    if output == 'text':
        print('''
            You are %.2f %s away from your nearest store:
            %s
            %s, 
            %s, %s %s
            ''' % 
            (store_details['Distance Away'], units, store_details['Store Name'], store_details['Address'],
                store_details['City'], store_details['State'], store_details['Zip Code']))
    else: # output == 'json'
        print(json.dumps(store_details, indent=4, sort_keys=True))
