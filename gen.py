import argparse
import csv
import json
import urllib.request
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('--ovd-info-dataset-url', default = 'https://api.repression.info/v1/data')
parser.add_argument('--ovd-info-addresses-csv', default = 'data/prisons_ovd.csv')
parser.add_argument('--output-json', default = 'data.json')
parser.add_argument('--output-js', default = 'data.js')
args = parser.parse_args()

ovd = json.load(urllib.request.urlopen(args.ovd_info_dataset_url))
print('Total prisoners:', ovd['total'])
print('First prisoner:', ovd['data'][0])

addresses = {row[0] : dict(name = row[0], mapmarkerkey = row[0], address = row[1], latlon = row[-1], url = 'https://google.com/maps/search/?' + urllib.parse.urlencode(dict(api = '1', query = row[-1]))) for row in list(csv.reader(open(args.ovd_info_addresses_csv)))[1:]}

sanitize_addr = lambda addr: addr.translate({ord('"') : '', ord('\u00A0'): ' ', ord('\xa0') : ' ', ord('\r'): ' ', ord('\n'): ' '}).strip()
   
data = [addresses[sanitized_addr] for prisoner in ovd['data'] for addr in set(prisoner["detention_center_ru"]) | set([prisoner["restraint_measure_location_ru"]]) | set(prisoner["penal_facility_ru"]) | set([prisoner["imprisonment_location_ru"]]) for sanitized_addr in filter(bool, [sanitize_addr(addr)]) if sanitized_addr in addresses] 

json.dump(data, open(args.output_json, 'w'), ensure_ascii = False, indent = 2)

open(args.output_js, 'w').write('data = ' + json.dumps(data, ensure_ascii = False, indent = 2))
