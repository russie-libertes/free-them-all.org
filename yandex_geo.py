import requests
import time

# Настройки
api_key = 'b21cfbe7-c069-48d1-b40c-4f56bb3c20b7'  # твой API-ключ
input_file = 'adr.txt'
output_file = 'gps_result.txt'

# Чтение адресов
with open(input_file, 'r', encoding='utf-8') as file:
    addresses = [line.strip() for line in file if line.strip()]

# Открываем файл для записи результатов
with open(output_file, 'w', encoding='utf-8') as out_file:
    for address in addresses:
        url = 'https://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': api_key,
            'geocode': address,
            'format': 'json'
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()

            feature_member = data['response']['GeoObjectCollection']['featureMember']
            
            if feature_member:
                pos = feature_member[0]['GeoObject']['Point']['pos']
                lon, lat = pos.split()
                out_file.write(f"{address} — {lat} — {lon}\n")
                print(f"✅ {address}: {lat}, {lon}")
            else:
                out_file.write(f"{address} — NOT FOUND\n")
                print(f"❌ {address}: координаты не найдены")

        except Exception as e:
            out_file.write(f"{address} — ERROR: {str(e)}\n")
            print(f"⚠️ {address}: ошибка {str(e)}")

        time.sleep(0.5)  # маленькая пауза между запросами, чтобы не забанили