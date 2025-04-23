import csv
import urllib.parse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Путь к ChromeDriver
chrome_path = r"C:\Windows\System32\chromedriver.exe"

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(chrome_path), options=options)
wait = WebDriverWait(driver, 10)

base_url = "https://www.rusprofile.ru/search?query="

with open("colony.txt", "r", encoding="utf-8") as file:
    colonies = [line.strip() for line in file if line.strip()]

results = []

for colony in colonies:
    encoded_query = urllib.parse.quote(colony, safe='')
    url = f"{base_url}{encoded_query}&type=ul"

    print(f"Обрабатываем: {colony}")
    driver.get(url)

    sleep(1)

    try:
        if "Попробуйте изменить поисковый запрос" in driver.page_source:
            print("  -> Не найдено")
            results.append((colony, "Не найдено"))
            continue

        address_block = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "address.company-info__text")))

        sleep(1)
        ActionChains(driver).move_to_element(address_block).click().perform()
        sleep(0.5)

        # Извлечение по частям
        def safe_get(selector):
            try:
                return address_block.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                return ""

        street = safe_get("[itemprop='streetAddress']")
        locality = safe_get("[itemprop='addressLocality']")
        region = safe_get("[itemprop='addressRegion']")
        postal_code = safe_get("[itemprop='postalCode']")
        country = "Россия"

        # Формируем адрес в нужном порядке
        parts = [street, locality, region, country, postal_code]
        formatted_address = ', '.join([part for part in parts if part])

        print(f"  -> Адрес: {formatted_address}")
        results.append((colony, formatted_address))

    except Exception as e:
        print(f"  !! Ошибка при обработке: {colony}")
        results.append((colony, "Ошибка"))

# Сохраняем в CSV
with open("results.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Поисковый запрос", "Адрес (обратный порядок)"])
    writer.writerows(results)

driver.quit()
print("Готово. Результаты записаны в results.csv.")
