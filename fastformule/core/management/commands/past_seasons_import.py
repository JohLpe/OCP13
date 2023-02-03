from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import os
from core.models import ChampionshipYear, Circuit, GPEvent,\
                        Driver, Team,\
                        SessionResults
import datetime
from .utils import GP_NAMES_EN_TO_FR, CIRCUIT_LOCATIONS,\
                   COUNTRIES_EN_TO_FR, SESSION_NAMES_EN_TO_FR,\
                   STATUS_EN_TO_FR
import fastf1 as ff
from slugify import slugify


class Command(BaseCommand):
    help = "first data import for previous seasons"

    def handle(self, *args, **options):


        load_dotenv()
        date = datetime.date.today()

        for year in range(1950, date.year):
            if ChampionshipYear.objects.filter(year=year):
                print("Year {} already added.".format(year))
            else:
                ChampionshipYear.objects.create(year=year)

            ff.Cache.enable_cache(os.getenv('CACHE_PATH'))
            my_schedule = ff.get_event_schedule(year,
                                                include_testing=False)
            max_round = my_schedule.RoundNumber.count()

            for round in range(1, (max_round.item()+1)):
                my_gp = ff.get_event(year, round)
                if GPEvent.objects.filter(year=year,
                                          gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName]):
                    print('{} of {} already created'.format(my_gp.EventName,
                                                            year))
                else:
                    if year > 1955 and my_gp.Location == 'Barcelona':
                        circuit, created = Circuit.objects.get_or_create(track_name="Circuit de Montjuïc",
                                                                         country=COUNTRIES_EN_TO_FR[my_gp.Country])
                        GPEvent.objects.create(year=ChampionshipYear.objects.get(year=year),
                                               gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName],
                                               gp_slug_name=slugify(GP_NAMES_EN_TO_FR[my_gp.EventName]),
                                               circuit=circuit,
                                               event_format=my_gp.EventFormat)
                    elif year > 1965 and my_gp.Location == 'California':
                        circuit, created = Circuit.objects.get_or_create(track_name="Circuit urbain de Long Beach",
                                                                         country=COUNTRIES_EN_TO_FR[my_gp.Country])
                        GPEvent.objects.create(year=ChampionshipYear.objects.get(year=year),
                                               gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName],
                                               gp_slug_name=slugify(GP_NAMES_EN_TO_FR[my_gp.EventName]),
                                               circuit=circuit,
                                               event_format=my_gp.EventFormat)
                    elif year >= 1982 and my_gp.Location == "Montreal":
                        circuit, created = Circuit.objects.get_or_create(track_name="Circuit Gilles-Villeneuve",
                                                                         country=COUNTRIES_EN_TO_FR[my_gp.Country])
                        GPEvent.objects.create(year=ChampionshipYear.objects.get(year=year),
                                               gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName],
                                               gp_slug_name=slugify(GP_NAMES_EN_TO_FR[my_gp.EventName]),
                                               circuit=circuit,
                                               event_format=my_gp.EventFormat)
                    elif year < 1990 and my_gp.Location == 'Spielberg':
                        circuit, created = Circuit.objects.get_or_create(track_name="Österreichring",
                                                                         country=COUNTRIES_EN_TO_FR[my_gp.Country])
                        GPEvent.objects.create(year=ChampionshipYear.objects.get(year=year),
                                               gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName],
                                               gp_slug_name=slugify(GP_NAMES_EN_TO_FR[my_gp.EventName]),
                                               circuit=circuit,
                                               event_format=my_gp.EventFormat)
                    elif year > 2010 and my_gp.Location == 'Spielberg':
                        circuit, created = Circuit.objects.get_or_create(track_name="Red Bull Ring",
                                                                         country=COUNTRIES_EN_TO_FR[my_gp.Country])
                        GPEvent.objects.create(year=ChampionshipYear.objects.get(year=year),
                                               gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName],
                                               gp_slug_name=slugify(GP_NAMES_EN_TO_FR[my_gp.EventName]),
                                               circuit=circuit,
                                               event_format=my_gp.EventFormat)
                    else:
                        circuit, created = Circuit.objects.get_or_create(track_name=CIRCUIT_LOCATIONS[my_gp.Location],
                                                                         country=COUNTRIES_EN_TO_FR[my_gp.Country])
                        GPEvent.objects.create(year=ChampionshipYear.objects.get(year=year),
                                               gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName],
                                               gp_slug_name=slugify(GP_NAMES_EN_TO_FR[my_gp.EventName]),
                                               circuit=circuit,
                                               event_format=my_gp.EventFormat)

                event_format = {'sprint': [2, 4, 5], 'conventional': [4, 5]}

                for session in event_format[my_gp.EventFormat]:
                    my_session = ff.get_session(year, round, session)
                    my_session.load(telemetry=False,
                                    weather=False,
                                    messages=False)

                    session_df = my_session.results[['FullName',
                                                     'FirstName',
                                                     'LastName',
                                                     'TeamName',
                                                     'Position',
                                                     'GridPosition',
                                                     'Q1', 'Q2', 'Q3',
                                                     'Time', 'Status',
                                                     'Points']]

                    session_df = session_df.reset_index()

                    default_deltatime = datetime.timedelta(days=0,
                                                           seconds=0,
                                                           microseconds=0,
                                                           milliseconds=0,
                                                           minutes=0,
                                                           hours=0,
                                                           weeks=0)

                    session_df = session_df.fillna({'Q1': default_deltatime,
                                                    'Q2': default_deltatime,
                                                    'Q3': default_deltatime,
                                                    'Time': default_deltatime,
                                                    'Position': "0"})

                    for row in session_df.index:

                        if Driver.objects.filter(full_name=session_df.loc[row, 'FullName']):
                            if session_df.loc[row, 'FullName'] == "Sergio Perez":
                                my_driver = Driver.objects.get(full_name="Sergio Pérez")
                            else:
                                my_driver = Driver.objects.get(full_name=session_df.loc[row, 'FullName'])
                        else:
                            Driver.objects.create(full_name=session_df.loc[row, 'FullName'],
                                                  first_name=session_df.loc[row, 'FirstName'],
                                                  last_name=session_df.loc[row, 'LastName'],
                                                  slug_name=slugify(session_df.loc[row, 'FullName']))
                            my_driver = Driver.objects.get(full_name=session_df.loc[row, 'FullName'])

                        my_team, created_team = Team.objects.get_or_create(name=session_df.loc[row, 'TeamName'])

                        current_gp_event = GPEvent.objects.get(year=year, gp_name=GP_NAMES_EN_TO_FR[my_gp.EventName])
                        current_gp_event.teams.add(my_team)
                        current_gp_event.drivers.add(my_driver)

                        if SessionResults.objects.filter(session_date=my_session.date.date(),
                                                         driver=my_driver):
                            print("Results for driver {} exist for session of {}".format(my_driver,
                                                                                        my_session.date.date()))
                        else:
                            SessionResults.objects.create(gp_id=current_gp_event,
                                                          session_type=SESSION_NAMES_EN_TO_FR[my_session.name],
                                                          session_date=my_session.date.date(),
                                                          driver=my_driver,
                                                          for_team=Team.objects.get(name=session_df.loc[row, 'TeamName']),
                                                          start_pos=int(session_df.loc[row, 'GridPosition']),
                                                          end_pos=int(session_df.loc[row, 'Position']),
                                                          q1=session_df.loc[row, 'Q1'],
                                                          q2=session_df.loc[row, 'Q2'],
                                                          q3=session_df.loc[row, 'Q3'],
                                                          race_time=session_df.loc[row, 'Time'],
                                                          finish_status=STATUS_EN_TO_FR[session_df.loc[row, 'Status']],
                                                          points=session_df.loc[row, 'Points'])

            ff.Cache.clear_cache(os.getenv('CACHE_PATH'))
