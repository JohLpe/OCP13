from django.db import models
from django.db.models.constraints import UniqueConstraint


class ChampionshipYear(models.Model):
    """F1 championship years"""

    year = models.IntegerField(primary_key=True)

    def __str__(self):
        return "Class ChampionshipYear, year {}".format(self.year)


class Circuit(models.Model):
    """Circuit information"""

    track_name = models.CharField(max_length=45, unique=True)
    country = models.CharField(max_length=30)

    def __str__(self):
        return "Class Circuit, name {}, id {}".format(self.track_name,
                                                      self.id)


class Team(models.Model):
    """Teams information"""

    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return "Class Team, name {}, id {}".format(self.name, self.id)


class Driver(models.Model):
    """Drivers information"""

    full_name = models.CharField(max_length=100, unique=True)
    slug_name = models.SlugField(allow_unicode=True, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    wiki_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return "Class Driver, name {}, id {}".format(self.full_name, self.id)


class GPEvent(models.Model):
    """Grand Prix event information"""

    year = models.ForeignKey(ChampionshipYear,
                             on_delete=models.CASCADE, to_field='year')
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE,
                                to_field='track_name')
    event_format = models.CharField(max_length=15)
    gp_name = models.CharField(max_length=40)
    gp_slug_name = models.SlugField(allow_unicode=True, null=True, blank=True)
    teams = models.ManyToManyField(Team)
    drivers = models.ManyToManyField(Driver)

    class Meta:
        constraints = [UniqueConstraint(fields=['year', 'gp_name'],
                                        name='unique_gp')]

    def __str__(self):
        return "Class GPEvent {} {}, id {}".format(self.gp_name,
                                                   self.year.year,
                                                   self.id)


class SessionResults(models.Model):
    """Results for GP event session"""

    gp_id = models.ForeignKey(GPEvent, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=25)
    session_date = models.DateField()
    driver = models.ForeignKey(Driver,
                               on_delete=models.CASCADE, to_field='full_name')
    for_team = models.ForeignKey(Team,
                                 on_delete=models.CASCADE, to_field='name',
                                 default='No Team Assigned')
    start_pos = models.IntegerField(null=True, blank=True)
    end_pos = models.IntegerField(null=True, blank=True)
    q1 = models.DurationField(null=True, blank=True)
    q2 = models.DurationField(null=True, blank=True)
    q3 = models.DurationField(null=True, blank=True)
    race_time = models.DurationField(null=True, blank=True)
    finish_status = models.CharField(max_length=100, null=True, blank=True)
    points = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['session_date', 'driver'],
                                        name='unique_results')]

    def __str__(self):
        return "Class SessionResults (id {}) for {} {}, driver {}".format(self.id,
                                                                          self.gp_id.gp_name,
                                                                          self.gp_id.year.year,
                                                                          self.driver.full_name)


class DriverChampionshipResults(models.Model):
    """Drivers' championship standing for each year"""

    year = models.ForeignKey(ChampionshipYear,
                             on_delete=models.CASCADE, to_field='year')
    driver = models.ForeignKey(Driver,
                               on_delete=models.CASCADE, to_field='full_name')
    driver_points = models.FloatField(null=True, blank=True)
    driver_rank = models.IntegerField(null=True, blank=True)
    for_team = models.ManyToManyField(Team)

    class Meta:
        constraints = [UniqueConstraint(fields=['year', 'driver'],
                                        name='unique_driver_standing')]

    def __str__(self):
        return "Class DriverChampionshipResults year {}, driver {}".format(self.year.year,
                                                                           self.driver.full_name)


class TeamChampionshipResults(models.Model):
    """Teams' constructor championship standing for each year"""

    year = models.ForeignKey(ChampionshipYear,
                             on_delete=models.CASCADE, to_field='year')
    team = models.ForeignKey(Team,
                             on_delete=models.CASCADE, to_field='name')
    team_points = models.FloatField()
    team_rank = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['year', 'team'],
                                        name='unique_team_standing')]

    def __str__(self):
        return "Class TeamChampionshipResults year {}, team {}".format(self.year.year,
                                                                       self.team.name)