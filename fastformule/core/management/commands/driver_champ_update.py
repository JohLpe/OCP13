from core.models import ChampionshipYear,\
                         Driver,\
                         DriverChampionshipResults
from django.core.management.base import BaseCommand,\
                                        CommandError
from pathlib import Path
import pandas as pd


class Command(BaseCommand):
    help = "import driver championship data from previous seasons"

    def handle(self, *args, **options):

        base = Path(__file__).parent
        real_path = Path(base, "additional_data", "yearlyDriversStandings.csv")
        csvFile = pd.read_csv(real_path)

        choice_pass = []

        for index in csvFile.index:
            try:
                check_driver_exists = Driver.objects.filter(full_name=csvFile.loc[index, 'Driver'])

                if check_driver_exists.count() == 1:
                    check_driver_ch = DriverChampionshipResults.objects.filter(year=csvFile.loc[index, 'year'],
                                                                               driver=check_driver_exists.first())

                    if check_driver_ch.count() == 1:

                        if check_driver_ch.first().driver_rank == int(csvFile.loc[index, 'Pos']):
                            pass

                        else:
                            check_driver_ch.update(driver_rank=int(csvFile.loc[index, 'Pos']))

                    elif check_driver_ch.count() == 0:

                        DriverChampionshipResults.objects.create(year=ChampionshipYear.objects.get(year=csvFile.loc[index, 'year']),
                                                                 driver=check_driver_exists.first(),
                                                                 driver_points=float(csvFile.loc[index, 'Points']),
                                                                 driver_rank=int(csvFile.loc[index, 'Pos']))

                    else:
                        for driver_ch_obj in check_driver_ch:
                            if driver_ch_obj.driver_rank == int(csvFile.loc[index, 'Pos']):
                                pass
                            else:
                                driver_ch_obj.delete()

                else:
                    recheck_driver_exists = Driver.objects.filter(full_name__icontains=csvFile.loc[index, 'Driver'])

                    if recheck_driver_exists.count() > 0:

                        for driver_icontains_filter in recheck_driver_exists:
                            print(driver_icontains_filter.full_name, "avec id ", driver_icontains_filter.id)

                        choice = input("I choose id : ")

                        if choice != "":

                            get_driver = Driver.objects.get(id=int(choice))

                            recheck_driver_ch = DriverChampionshipResults.objects.filter(year=csvFile.loc[index, 'year'],
                                                                                         driver=get_driver)
                            if recheck_driver_ch.count() == 1:

                                if recheck_driver_ch.first().driver_rank == int(csvFile.loc[index, 'Pos']):
                                    pass

                                else:
                                    recheck_driver_ch.update(driver_rank=int(csvFile.loc[index, 'Pos']))

                            elif recheck_driver_ch.count() == 0:

                                DriverChampionshipResults.objects.create(year=ChampionshipYear.objects.get(year=csvFile.loc[index, 'year']),
                                                                         driver=get_driver,
                                                                         driver_points=float(csvFile.loc[index, 'Points']),
                                                                         driver_rank=int(csvFile.loc[index, 'Pos']))
                        else:
                            choice_pass.append("problem with {} in {}".format(csvFile.loc[index, 'Driver'],
                                                                              csvFile.loc[index, 'year']))

            except Exception as e:
                raise CommandError("Following error happened: '%s' " % e)
        print(choice_pass)
