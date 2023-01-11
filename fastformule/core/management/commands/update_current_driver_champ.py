from core.models import DriverChampionshipResults
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Manual updates current driver standing"

    def handle(self, *args, **options):

        for standing in DriverChampionshipResults.objects.filter(year=2022):

            print(standing.driver.full_name)

            new_rank = input("Current rank : ")
            new_points = input("Current points : ")

            DriverChampionshipResults.objects.filter(driver=standing.driver).update(driver_rank=int(new_rank),
                                                                                    driver_points=float(new_points))
