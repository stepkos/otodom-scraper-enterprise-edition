from time import sleep

import requests
from lxml import html
from yarl import URL

from modules.apartments.models import Apartment
from modules.scrapers.constants.for_scraper import HTTP_HEADERS
from modules.scrapers.services.scraper_listview import apartments_iterator
from modules.scrapers.services.scraper_subview import scrape_apartment_details


def get_listview_aparts():
    url = URL(
        "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing"
    )
    for apartment in apartments_iterator(url):
        print(apartment)
        try:
            apartment.save()
        except Exception as e:  # Duplicate key error
            print(e)


# moze jakis status (waiting for details, completed, deleted, waiting for update)
# dodaj pole real_floor i pobieraj piętro z subviewa
def update_aparts_with_subview():
    apartments_without_details = Apartment.objects.filter(
        details__isnull=True, was_deleted=False
    )
    count = apartments_without_details.count()
    for apartment in apartments_without_details:
        count -= 1
        url = URL("https://www.otodom.pl" + apartment.subpage)
        response = requests.get(
            str(url), headers=HTTP_HEADERS, timeout=10
        )  # timeotu moze wyrzucic
        if response.status_code == 410:
            print("The offer was deleted. Skipping...")
            apartment.was_deleted = True
            apartment.save()
            continue
        elif response.status_code != 200:
            print("Failed to fetch page. Http code:", response.status_code)
            print("Sleeping for 30 seconds...")
            sleep(30)
            continue

        a = scrape_apartment_details(html.fromstring(response.text))
        a.apartment = apartment
        try:
            a.save()
        except Exception as e:
            print(e)

        print("Apartment saved successfully!. Left:", count, "apartments.")
        # sleep(.2)
        # if i % 30 == 0:
        #     print("Sleeping for 30 seconds...")
        #     sleep(30)


def fix_max_floor():
    apartments_max_floor_graten_than_floor = Apartment.objects.filter(
        details__max_floor__gt=F("floor")
    )
    count = apartments_max_floor_graten_than_floor.count()
    for apartment in apartments_max_floor_graten_than_floor:
        count -= 1
        print(apartment.floor, apartment.details.max_floor)
        ...
        # url = URL("https://www.otodom.pl" + apartment.subpage)
        # response = requests.get(str(url), headers=HTTP_HEADERS, timeout=10)  # timeotu moze wyrzucic
        # if response.status_code == 410:
        #     print("The offer was deleted. Skipping...")
        #     apartment.was_deleted = True
        #     apartment.save()
        #     continue
        # elif response.status_code != 200:
        #     print("Failed to fetch page. Http code:", response.status_code)
        #     print("Sleeping for 30 seconds...")
        #     sleep(30)
        #     continue
        #
        # a = scrape_apartment_details(html.fromstring(response.text))
        # a.apartment = apartment
        # try:
        #     a.save()
        # except Exception as e:
        #     print(e)
        #
        # print("Apartment saved successfully!. Left:", count, "apartments.")
        #
