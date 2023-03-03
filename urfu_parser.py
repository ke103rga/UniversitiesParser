from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService

chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
chrome_service = ChromeService("chromedriver_win32\\chromedriver.exe")
chrome_service.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(executable_path="chromedriver_win32\\chromedriver.exe")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_position(100, 150)
driver.set_window_size(1, 1)
url = "https://urfu.ru/ru/ratings/"

ENTRANT_SNILS = "snils"
table_ids = ["1279368728", "285468005"]


def get_rating_page(url, driver):
    driver.get(url)
    rows = driver.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) != 0:
            if tds[0].text == "Институт строительства и архитектуры":
                elem = tds[1].find_element(By.TAG_NAME, "a")
                elem.click()
                time.sleep(10)
                break
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def parse_table(soup, id):
    rate = {"univercity": "УрФУ", "speciality": "", "rate": "", "agreement_rate": "", "plan": ""}

    head = soup.find("table", id=id)
    rate["speciality"] = head.find("tr").find_all("td")[-1].text

    rate["plan"] = get_plan(head.find_next("div").text)

    building_table = head.find_next("table", class_="supp").find_next("table", class_="supp")
    counter = 0
    agreement_counter = 0
    rows = building_table.find_all("tr")
    for row in rows:
        if len(row.find_all("th")) == 0:
            tds = row.find_all("td")
            counter += 1
            if tds[2].text.lower() == "да":
                agreement_counter += 1
            if tds[0].text == ENTRANT_SNILS:
                break
    rate["rate"] = counter
    rate["agreement_rate"] = agreement_counter

    return rate


def get_plan(text):
    pattern = "план приема"
    start_index = text.index(pattern) + len(pattern)
    plan = text[start_index:].strip()
    if plan.isdigit():
        return plan
    else:
        return "error"


def parser():
    try:
        entrant_info = []

        soup = get_rating_page(url, driver)
        for id in table_ids:
            entrant_info.append(parse_table(soup, id))

        return entrant_info
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()



