from core.models import ChampionshipYear,\
                         Team,\
                         TeamChampionshipResults
from django.core.management.base import BaseCommand,\
                                        CommandError
from pathlib import Path
import pandas as pd


class Command(BaseCommand):
    help = "import constructor championship data from previous seasons"

    def handle(self, *args, **options):


        TeamChampionshipResults.objects.all().exclude(year=2022).delete()

        base = Path(__file__).parent
        real_path = Path(base, "additional_data", "yearlyTeamsStandings.csv")
        csvFile = pd.read_csv(real_path)

        choice_pass = []

        for index in csvFile.index:
            try:
                check_team_exists = Team.objects.filter(name=csvFile.loc[index, 'Constructor'])

                if check_team_exists.count() == 1:
                    check_cons_ch = TeamChampionshipResults.objects.filter(year=csvFile.loc[index, 'year'],
                                                                           team=check_team_exists.first())

                    if check_cons_ch.count() == 1:

                        if check_cons_ch.first().team_rank == int(csvFile.loc[index, 'Pos']):
                            pass

                        else:
                            check_cons_ch.update(team_rank=int(csvFile.loc[index, 'Pos']))

                    elif check_cons_ch.count() == 0:

                        TeamChampionshipResults.objects.create(year=ChampionshipYear.objects.get(year=csvFile.loc[index, 'year']),
                                                               team=check_team_exists.first(),
                                                               team_points=float(csvFile.loc[index, 'Points']),
                                                               team_rank=int(csvFile.loc[index, 'Pos']))

                    else:
                        for cons_ch_obj in check_cons_ch:
                            if cons_ch_obj.team_rank == int(csvFile.loc[index, 'Pos']):
                                pass
                            else:
                                cons_ch_obj.delete()

                else:
                    recheck_team_exists = Team.objects.filter(name__icontains=csvFile.loc[index, 'Constructor'])

                    if recheck_team_exists.count() > 0:

                        for team_icontains_filter in recheck_team_exists:
                            print(team_icontains_filter.name, "avec id ", team_icontains_filter.id)

                        choice = input("I choose id : ")

                        if choice != "":

                            get_team = Team.objects.get(id=int(choice))

                            recheck_cons_ch = TeamChampionshipResults.objects.filter(year=csvFile.loc[index, 'year'],
                                                                                     team=get_team)
                            if recheck_cons_ch.count() == 1:

                                if recheck_cons_ch.first().team_rank == int(csvFile.loc[index, 'Pos']):
                                    pass

                                else:
                                    recheck_cons_ch.update(team_rank=int(csvFile.loc[index, 'Pos']))

                            elif recheck_cons_ch.count() == 0:

                                TeamChampionshipResults.objects.create(year=ChampionshipYear.objects.get(year=csvFile.loc[index, 'year']),
                                                                        team=get_team,
                                                                        team_points=float(csvFile.loc[index, 'Points']),
                                                                        team_rank=int(csvFile.loc[index, 'Pos']))
                        else:
                            choice_pass.append("problem with {} in {}".format(csvFile.loc[index, 'Constructor'],
                                                                              csvFile.loc[index, 'year']))

            except Exception as e:
                raise CommandError("Following error happened: '%s' " % e)
        print(choice_pass)
