import json

# Загрузка данных
with open('persecution_data_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Множество для всех уникальных значений
unique_places = set()

# Обход записей
for record in data.get("data", []):
    unique_places.update(map(str.strip, record.get("penal_facility_ru", [])))
    unique_places.update(map(str.strip, record.get("detention_center_ru", [])))
    loc = record.get("imprisonment_location_ru")
    if loc:
        unique_places.add(loc.strip())

# Очистка строк: убираем кавычки, NBSP, заменяем переносы внутри строки
cleaned_places = set()
for place in unique_places:
    cleaned = (
        place.replace('"', '')            # Удаляем двойные кавычки
             .replace('\u00A0', ' ')      # NBSP на пробел
             .replace('\xa0', ' ')        # дублирующий NBSP
             .replace('\r', ' ')          # Переносы строки на пробел
             .replace('\n', ' ')          # То же самое
             .strip()
    )
    cleaned_places.add(cleaned)

# Сохраняем результат
with open('unique_places.txt', 'w', encoding='utf-8') as f:
    for place in sorted(cleaned_places):
        f.write(place + '\n')

print("Готово! Чистый список учреждений сохранён в 'unique_places.txt'")