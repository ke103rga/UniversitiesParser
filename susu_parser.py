from bs4 import BeautifulSoup
import requests
import os
import re


urls = {"building_url": "https://abit.susu.ru/rating/2022/list.php?35093/2/1",
        "building_unique_url": "https://abit.susu.ru/rating/2022/list.php?35090/2/1"}

entrant_number = "18439"


def get_html_file(file_name, url, dir_path="C:/Users/Виктория/PycharmProjects/UniversitiesParser/rates"):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


    with open(f"{dir_path}/{file_name}.html", "w", encoding="utf-8") as file:
        q = requests.get(url)
        text = q.text

        file.write(text)


def count_agreements(soup, rate):
    entrants = soup.find_all("tr")
    entrants = entrants[1:rate]

    count = 0
    for entrant in entrants:
        agreement = entrant.find_all("td")[3].text
        if agreement.lower() == "да":
            count += 1

    return count


def parse_page(html_file, dir_path="C:/Users/Виктория/PycharmProjects/UniversitiesParser/rates"):
    with open(f"{dir_path}/{html_file}.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    rates = {"rate": "", "agreement_rate": ""}

    entrant = soup.find("td", string=re.compile(entrant_number)).find_parent("tr")
    rates["rate"] = entrant.find("td", class_="r").text

    rates["agreement_rate"] = count_agreements(soup, int(rates["rate"])) + 1

    return rates


def parser():
    entrant_info = []

    for name, url in urls.items():
        get_html_file(name, url)

        entrant_info.append(parse_page(name))

    print(entrant_info)


parser()
