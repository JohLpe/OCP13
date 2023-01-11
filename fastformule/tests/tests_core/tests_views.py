from django.test import TestCase, Client
from core.models import ChampionshipYear,\
                        Circuit,\
                        Team,\
                        Driver,\
                        GPEvent,\
                        SessionResults,\
                        DriverChampionshipResults,\
                        TeamChampionshipResults
import datetime
from django.urls import reverse


class ViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.c = Client()
        cls.championshipyear = ChampionshipYear.objects.create(year=2020)
        cls.ch_year_all = ChampionshipYear.objects.all()

        cls.circuit = Circuit.objects.create(track_name="Le Mans",
                                             country="France")
        cls.circuit_all = Circuit.objects.all()

        cls.team = Team.objects.create(name="Team Test")
        cls.team_all = Team.objects.all()

        cls.driver = Driver.objects.create(full_name="Driver Test",
                                           slug_name="driver-test",
                                           first_name="Driver",
                                           last_name="Test",
                                           nationality="Français",
                                           dob=datetime.date(1999, 3, 27))
        cls.driver_all = Driver.objects.all()

        cls.gpevent = GPEvent.objects.create(year=cls.ch_year_all.first(),
                                             circuit=cls.circuit_all.first(),
                                             event_format="Conventionnel",
                                             gp_name="Grand Prix du test",
                                             gp_slug_name="grand-prix-du-test")
        cls.gpevent_all = GPEvent.objects.all()

        cls.session_race = SessionResults.objects.create(gp_id=cls.gpevent_all.first(),
                                                         session_type="Course",
                                                         session_date=datetime.date(2020, 3, 22),
                                                         driver=cls.driver_all.first(),
                                                         for_team=cls.team_all.first(),
                                                         start_pos=2,
                                                         end_pos=1,
                                                         race_time=datetime.timedelta(days=0,
                                                                                      seconds=36,
                                                                                      microseconds=0,
                                                                                      milliseconds=345,
                                                                                      minutes=27,
                                                                                      hours=1,
                                                                                      weeks=0),
                                                         finish_status="Fini",
                                                         points=25.0)
        cls.session_quali = SessionResults.objects.create(gp_id=cls.gpevent_all.first(),
                                                          session_type="Qualifications",
                                                          session_date=datetime.date(2020, 3, 21),
                                                          driver=cls.driver_all.first(),
                                                          for_team=cls.team_all.first(),
                                                          end_pos=1,
                                                          q1=datetime.timedelta(days=0,
                                                                                seconds=24,
                                                                                microseconds=0,
                                                                                milliseconds=345,
                                                                                minutes=1,
                                                                                hours=0,
                                                                                weeks=0),
                                                          q2=datetime.timedelta(days=0,
                                                                                seconds=24,
                                                                                microseconds=0,
                                                                                milliseconds=456,
                                                                                minutes=1,
                                                                                hours=0,
                                                                                weeks=0),
                                                          q3=datetime.timedelta(days=0,
                                                                                seconds=23,
                                                                                microseconds=0,
                                                                                milliseconds=998,
                                                                                minutes=1,
                                                                                hours=0,
                                                                                weeks=0))
        cls.session_all = SessionResults.objects.all()

        cls.d_ch_rslts = DriverChampionshipResults.objects.create(year=cls.ch_year_all.first(),
                                                                  driver=cls.driver_all.first(),
                                                                  driver_rank=1,
                                                                  driver_points=398.0)
        cls.d_ch_rslts_all = DriverChampionshipResults.objects.all()

        cls.t_ch_rslts = TeamChampionshipResults.objects.create(year=cls.ch_year_all.first(),
                                                                team=cls.team_all.first(),
                                                                team_points=586.5,
                                                                team_rank=1)
        cls.t_ch_rslts_all = TeamChampionshipResults.objects.all()

    def test_seasons_page(self):

        response = self.c.get(reverse('seasons'))
        self.assertEqual(response.status_code, 200)

    def test_calendar_page(self):

        response = self.c.get(reverse('calendar', args=[self.championshipyear.year]))
        self.assertEqual(response.status_code, 200)

    def test_current_year(self):

        response = self.c.get(reverse('current'))
        self.assertEqual(response.status_code, 200)

    def test_gp_results(self):

        response = self.c.get(reverse('gp_results', args=[self.championshipyear.year, self.gpevent.gp_slug_name]))
        self.assertEqual(response.status_code, 200)

    def test_driver_page(self):

        response = self.c.get(reverse('driver_page'))
        self.assertEqual(response.status_code, 200)

    def test_driver_info_page(self):

        response = self.c.get(reverse('driver_info', args=[self.driver.slug_name]))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):

        response = self.c.get(reverse('search_results') + '?q=driver+test')
        self.assertEqual(response.status_code, 200)
