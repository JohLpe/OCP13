from core.models import TeamChampionshipResults
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Manual updates current constructor standing"

    def handle(self, *args, **options):

        for standing in TeamChampionshipResults.objects.filter(year=2022):

            print(standing.team.name)

            new_rank = input("Current rank : ")
            new_points = input("Current points : ")

            TeamChampionshipResults.objects.filter(team=standing.team).update(team_rank=int(new_rank),
                                                                              team_points=float(new_points))
