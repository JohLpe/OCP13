from django.test import TestCase
from core.models import ChampionshipYear,\
                        Circuit,\
                        Team,\
                        Driver,\
                        GPEvent,\
                        SessionResults,\
                        DriverChampionshipResults,\
                        TeamChampionshipResults
import datetime


class TestModels(TestCase):
    """Tests the models from core app"""

    @classmethod
    def setUpTestData(cls):
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

    def test_championshipyear_was_created(self):
        """Test the creation of a ChampionshipYear instance"""

        self.assertEqual(self.ch_year_all.count(), 1)
        self.assertIsInstance(self.ch_year_all.first().year, int)
        self.assertEqual(self.ch_year_all.first().year, 2020)

    def test_circuit_was_created(self):
        """Test the creation of a Circuit instance"""

        self.assertEqual(self.circuit_all.count(), 1)
        self.assertIsInstance(self.circuit_all.first().track_name, str)
        self.assertEqual(self.circuit_all.first().track_name, "Le Mans")
        self.assertIsInstance(self.circuit_all.first().country, str)
        self.assertEqual(self.circuit_all.first().country, "France")

    def test_team_was_created(self):
        """Test the creation of a Team instance"""

        self.assertEqual(self.team_all.count(), 1)
        self.assertIsInstance(self.team_all.first().name, str)
        self.assertEqual(self.team_all.first().name, "Team Test")

    def test_driver_was_created(self):
        """Test the creation of a Driver instance"""

        self.assertEqual(self.driver_all.count(), 1)
        self.assertIsInstance(self.driver_all.first().full_name, str)
        self.assertEqual(self.driver_all.first().full_name, "Driver Test")
        self.assertIsInstance(self.driver_all.first().slug_name, str)
        self.assertEqual(self.driver_all.first().slug_name, "driver-test")
        self.assertIsInstance(self.driver_all.first().first_name, str)
        self.assertEqual(self.driver_all.first().first_name, "Driver")
        self.assertIsInstance(self.driver_all.first().last_name, str)
        self.assertEqual(self.driver_all.first().last_name, "Test")
        self.assertIsInstance(self.driver_all.first().nationality, str)
        self.assertEqual(self.driver_all.first().nationality, "Français")
        self.assertIsInstance(self.driver_all.first().dob, datetime.date)
        self.assertEqual(self.driver_all.first().dob, datetime.date(1999, 3, 27))

    def test_gpevent_was_created(self):
        """Test the creation of a GPEvent instance"""

        self.assertEqual(self.gpevent_all.count(), 1)
        self.assertIsInstance(self.gpevent_all.first().year.year, int)
        self.assertEqual(self.gpevent_all.first().year.year, 2020)
        self.assertIsInstance(self.gpevent_all.first().circuit.track_name, str)
        self.assertEqual(self.gpevent_all.first().circuit.track_name, "Le Mans")
        self.assertIsInstance(self.gpevent_all.first().event_format, str)
        self.assertEqual(self.gpevent_all.first().event_format, "Conventionnel")
        self.assertIsInstance(self.gpevent_all.first().gp_name, str)
        self.assertEqual(self.gpevent_all.first().gp_name, "Grand Prix du test")
        self.assertIsInstance(self.gpevent_all.first().gp_slug_name, str)
        self.assertEqual(self.gpevent_all.first().gp_slug_name, "grand-prix-du-test")


    def test_sessionresults_were_created(self):
        """Test the creation of 2 SessionResults instances"""

        self.assertEqual(self.session_all.count(), 2)

        self.assertIsInstance(self.session_race.gp_id.id, int)
        self.assertIsInstance(self.session_race.gp_id.gp_name, str)
        self.assertEqual(self.session_race.gp_id.gp_name, "Grand Prix du test")
        self.assertIsInstance(self.session_race.session_type, str)
        self.assertEqual(self.session_race.session_type, "Course")
        self.assertIsInstance(self.session_race.session_date, datetime.date)
        self.assertEqual(self.session_race.session_date, datetime.date(2020, 3, 22))
        self.assertIsInstance(self.session_race.driver.full_name, str)
        self.assertEqual(self.session_race.driver.full_name, "Driver Test")
        self.assertIsInstance(self.session_race.for_team.name, str)
        self.assertEqual(self.session_race.for_team.name, "Team Test")
        self.assertIsInstance(self.session_race.start_pos, int)
        self.assertEqual(self.session_race.start_pos, 2)
        self.assertIsInstance(self.session_race.end_pos, int)
        self.assertEqual(self.session_race.end_pos, 1)
        self.assertIsInstance(self.session_race.finish_status, str)
        self.assertEqual(self.session_race.finish_status, "Fini")
        self.assertIsInstance(self.session_race.points, float)
        self.assertEqual(self.session_race.points, 25.0)

        self.assertIsInstance(self.session_quali.gp_id.id, int)
        self.assertIsInstance(self.session_quali.gp_id.gp_name, str)
        self.assertEqual(self.session_quali.gp_id.gp_name, "Grand Prix du test")
        self.assertIsInstance(self.session_quali.session_type, str)
        self.assertEqual(self.session_quali.session_type, "Qualifications")
        self.assertIsInstance(self.session_quali.session_date, datetime.date)
        self.assertEqual(self.session_quali.session_date, datetime.date(2020, 3, 21))
        self.assertIsInstance(self.session_quali.driver.full_name, str)
        self.assertEqual(self.session_quali.driver.full_name, "Driver Test")
        self.assertIsInstance(self.session_quali.for_team.name, str)
        self.assertEqual(self.session_quali.for_team.name, "Team Test")
        self.assertIsInstance(self.session_quali.end_pos, int)
        self.assertEqual(self.session_quali.end_pos, 1)
        self.assertIsInstance(self.session_quali.q1, datetime.timedelta)
        self.assertEqual(self.session_quali.q1, datetime.timedelta(days=0,
                                                                   seconds=24,
                                                                   microseconds=0,
                                                                   milliseconds=345,
                                                                   minutes=1,
                                                                   hours=0,
                                                                   weeks=0))
        self.assertIsInstance(self.session_quali.q2, datetime.timedelta)
        self.assertEqual(self.session_quali.q2, datetime.timedelta(days=0,
                                                                   seconds=24,
                                                                   microseconds=0,
                                                                   milliseconds=456,
                                                                   minutes=1,
                                                                   hours=0,
                                                                   weeks=0))
        self.assertIsInstance(self.session_quali.q3, datetime.timedelta)
        self.assertEqual(self.session_quali.q3, datetime.timedelta(days=0,
                                                                   seconds=23,
                                                                   microseconds=0,
                                                                   milliseconds=998,
                                                                   minutes=1,
                                                                   hours=0,
                                                                   weeks=0))

    def test_driverchampionshipresults_was_created(self):
        """Test the creation of a DriverChampionshipResults instance"""

        self.assertEqual(self.d_ch_rslts_all.count(), 1)
        self.assertIsInstance(self.d_ch_rslts_all.first().year.year, int)
        self.assertEqual(self.d_ch_rslts_all.first().year.year, 2020)
        self.assertIsInstance(self.d_ch_rslts_all.first().driver.full_name, str)
        self.assertEqual(self.d_ch_rslts_all.first().driver.full_name, "Driver Test")
        self.assertIsInstance(self.d_ch_rslts_all.first().driver_rank, int)
        self.assertEqual(self.d_ch_rslts_all.first().driver_rank, 1)
        self.assertIsInstance(self.d_ch_rslts_all.first().driver_points, float)
        self.assertEqual(self.d_ch_rslts_all.first().driver_points, 398.0)

    def test_teamchampionshipresults_was_created(self):
        """test the creation of a TeamChampionshResults instance"""

        self.assertEqual(self.t_ch_rslts_all.count(), 1)
        self.assertIsInstance(self.t_ch_rslts_all.first().year.year, int)
        self.assertEqual(self.t_ch_rslts_all.first().year.year, 2020)
        self.assertIsInstance(self.t_ch_rslts_all.first().team.name, str)
        self.assertEqual(self.t_ch_rslts_all.first().team.name, "Team Test")
        self.assertIsInstance(self.t_ch_rslts_all.first().team_points, float)
        self.assertEqual(self.t_ch_rslts_all.first().team_points, 586.5)
        self.assertIsInstance(self.t_ch_rslts_all.first().team_rank, int)
        self.assertEqual(self.t_ch_rslts_all.first().team_rank, 1)
