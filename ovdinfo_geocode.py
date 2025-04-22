import os
import json
import argparse
import urllib.request
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('--dotenv', default = '.env')
parser.add_argument('--google-api-key')
parser.add_argument('--verbose-http', action = 'store_true')
parser.add_argument('--ovdinfo-dataset-url', default = 'https://api.repression.info/v1/data')
parser.add_argument('--google-geocoding-api-url', default = 'https://maps.googleapis.com/maps/api/geocode/json?address={ADDRESS}&key={GOOGLE_API_KEY}', help = 'https://developers.google.com/maps/documentation/urls/get-started')
parser.add_argument('--google-places-api-url', default = 'https://places.googleapis.com/v1/places:searchText', help = 'https://developers.google.com/maps/documentation/places/web-service/text-search')
parser.add_argument('--cache-json-path')
parser.add_argument('--cache-override', action = 'store_true')
args = parser.parse_args()

secrets = {}
if args.dotenv and os.path.exists(args.dotenv):
    secrets.update({ line.strip().split('=', maxsplit = 1)[0] : line.strip().split('=', maxsplit = 1)[1].split('#')[0] for line in open(args.dotenv) if line.strip() and not line.strip().startswith('#')})
if args.google_api_key:
    secrets['GOOGLE_API_KEY'] = args.google_api_key
cache = {}
if args.cache_json_path and os.path.exists(args.cache_json_path):
    with open(args.cache_json_path) as f:
        cache.update(json.load(f))

if args.verbose_http:
    import http.client
    http.client.HTTPConnection.debuglevel = 1

ovd = json.load(urllib.request.urlopen(args.ovdinfo_dataset_url))
print('Total prisoners:', ovd['total'])

for prisoner in ovd['data']:
    addresses = set(prisoner["detention_center_ru"]) | set([prisoner["restraint_measure_location_ru"]]) | set(prisoner["penal_facility_ru"]) | set([prisoner["imprisonment_location_ru"]])
    for address in filter(bool, addresses):
        address = address.translate({ord('«') : ' ', ord('»') : ' ', ord('"') : ' ', ord("№") : ' ', ord('|') : ','}).replace('  ', ' ')
        if address not in cache or args.cache_override:
            places = json.load(urllib.request.urlopen(urllib.request.Request(args.google_places_api_url, data = json.dumps(dict(textQuery = address)).encode('utf-8'), method = 'POST', headers = {'Content-Type': 'application/json', 'X-Goog-Api-Key' : secrets.get('GOOGLE_API_KEY', ''), 'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.googleMapsUri,places.location'})))
            print(places)
            
            url = args.google_geocoding_api_url.format(GOOGLE_API_KEY = secrets.get('GOOGLE_API_KEY', ''), ADDRESS = urllib.parse.quote_plus(address) )
            print(url)
            geo = json.load(urllib.request.urlopen(url))

            print('Geo status:', geo['status'], ', results:', len(geo['results']))
            assert 'OK' == geo['status']
            for geores in geo['results']:
                print(address)
                print(geores)
                placeid = geores['place_id']
                lat, lng = map(geores['geometry']['location'].get, ['lat', 'lng'])
                mapsurl = 'https://google.com/maps/search/?' + urllib.parse.urlencode(dict(api = '1', query = f'{lat},{lng}', query_place_id = placeid))
                print(mapsurl)
                print()
                if len(geo['results']) == 1:
                    cache[address] = mapsurl
            
            import sys; sys.exit(0)

if args.cache_json_path:
    json.dump(open(args.cache_json_path, 'w'), cache, ensure_ascii = False, indent = 2, sort_keys = True)
