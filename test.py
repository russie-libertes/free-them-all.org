import os
import json
import argparse
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--dotenv', default = '.env')
parser.add_argument('--google-geocoding-api-key')
parser.add_argument('--google-gemini-api-key')
parser.add_argument('--ovd-info-dataset-url', default = 'https://api.repression.info/v1/data')
parser.add_argument('--google-geocoding-api-url', default = 'https://maps.googleapis.com/maps/api/geocode/json?address=${ADDRESS}&key=${GOOGLE_GEOCODING_API_KEY}')
parser.add_argument('--google-gemini-api-url', default = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GOOGLE_GEMINI_API_KEY}')
args = parser.parse_args()

secrets = {}
if args.dotenv and os.path.exists(args.dotenv):
    secrets.update({ line.strip().split('=', maxsplit = 1)[0] : line.strip().split('=', maxsplit = 1)[1].split('#')[0] for line in open(args.dotenv) if line.strip() and not line.strip().startswith('#')})
if args.google_geocoding_api_key:
    secrets['GOOGLE_GEOCODING_API_KEY'] = args.google_geocoding_api_key
if args.google_gemini_api_key:
    secrets['GOOGLE_GEMINI_API_KEY'] = args.google_gemini_api_key
    
ovd = json.load(urllib.request.urlopen(args.ovd_info_dataset_url))
print('Total prisoners:', ovd['total'])
print('First prisoner:', ovd['data'][0])

address = '1600 Amphitheatre Parkway, Mountain+View, CA'
geo = json.load(urllib.request.urlopen(args.google_geocoding_api_url.replace('${GOOGLE_GEOCODING_API_KEY}', secrets.get('GOOGLE_GEOCODING_API_KEY', '')).replace('${ADDRESS}', address.replace(' ', '+'))))
print('Geo status:', geo['status'])
print('First geo:', geo['results'][0])

#curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}" -H 'Content-Type: application/json' -X POST  -d '{ "contents": [{ "parts":[{"text": "Explain how AI works"}] }] }'

aireq = dict(contents = [dict(parts = [dict(text = 'Explain how AI works')])])
ai = json.load(urllib.request.urlopen(urllib.request.Request(args.google_gemini_api_url.replace('${GOOGLE_GEMINI_API_KEY}', secrets.get('GOOGLE_GEMINI_API_KEY', '')), json.dumps(aireq, ensure_ascii = False).encode('utf-8'), {'Content-Type' : 'application/json'})))
print(ai)
