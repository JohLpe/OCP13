from django.core.management.base import BaseCommand, CommandError
from core.models import Driver
from pathlib import Path
import pandas as pd
from .utils import NATIONALITY_EN_TO_FR
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = "updates drivers data from csv file"

    def handle(self, *args, **options):

        base = Path(__file__).parent
        real_path = Path(base, "additional_data", "drivers.csv")
        csvFile = pd.read_csv(real_path)

        for index in csvFile.index:
            try:
                fullname = csvFile.loc[index, 'forename']+" "+csvFile.loc[index, 'surname']
                my_driver = Driver.objects.filter(full_name__icontains=fullname)

                response = requests.get(url=csvFile.loc[index, 'url'])
                soup = BeautifulSoup(response.content, 'html.parser')
                if soup.find(class_='interwiki-fr') is None:
                    response = requests.get(url=csvFile.loc[index, 'url']+"_(racing_driver)")
                    soup = BeautifulSoup(response.content, 'html.parser')
                    print(fullname)
                    print(type(soup))
                language_links = soup.find(class_='interwiki-fr').find_all('a')
                for link in language_links:
                    fr_link = link['href']

                if my_driver.count() == 1:
                    my_driver.update(nationality=NATIONALITY_EN_TO_FR[csvFile.loc[index, 'nationality']],
                                     dob=csvFile.loc[index, 'dob'],
                                     wiki_link=fr_link)

                elif my_driver.count() > 1:
                    for available_drivers in my_driver:
                        print(available_drivers.first_name, available_drivers.last_name, available_drivers.id)

                    choice = input("Pick relevant driver ID: ")

                    if choice != "":
                        Driver.objects.filter(id=int(choice)).update(nationality=NATIONALITY_EN_TO_FR[csvFile.loc[index, 'nationality']],
                                                                     dob=csvFile.loc[index, 'dob'],
                                                                     wiki_link=fr_link)

            except Exception as e:
                raise CommandError("Following error happened: '%s' " % e)
