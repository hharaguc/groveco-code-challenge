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

def parse_stores_file():
    store_locations = DictReader(open("./store-locations.csv"))

    # for store in store_locations:
        # print(store)


if __name__ == '__main__':
    expected_units = ['mi', 'km']
    expected_outputs = ['text', 'json']

    # parse and validate command line arguments
    args = docopt(__doc__, version=VERSION)
    start_loc = args['--address'] if args['--address'] else args['--zip']
    units = args['--units']
    output = args['--output']

    if units not in expected_units:
        exit(units + ' is not a valid --unit argument.' + __doc__)
    if output not in expected_outputs:
        exit(output + ' is not a valid --output argument.' + __doc__)

    print(start_loc)
    print(units)
    print(args)
    parse_stores_file()
