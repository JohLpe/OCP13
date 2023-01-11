from django.shortcuts import render
from .models import ChampionshipYear, GPEvent,\
                    SessionResults,\
                    Driver,\
                    Circuit,\
                    DriverChampionshipResults,\
                    TeamChampionshipResults
import datetime
from math import trunc
import string
import re
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from slugify import slugify


@ensure_csrf_cookie
def seasons_page(request):
    """Renders seasons selection page"""

    date = datetime.date.today()
    decades_filter = []
    for nb in range(195, trunc(date.year/10)+1):
        decades_filter.append(nb)

    seasons = dict.fromkeys(decades_filter)

    for decade in decades_filter:
        years_in_decade = []
        decade_schedule = ChampionshipYear.objects.filter(year__startswith=decade).exclude(year=date.year)
        for year in decade_schedule:
            years_in_decade.append(year.year)
        seasons[decade] = years_in_decade

    by_country = []
    by_circuit = Circuit.objects.all().order_by('country')
    for track in by_circuit:
        by_country.append(track.country)
    by_country = dict.fromkeys(list(dict.fromkeys(by_country)))
    for country_key in by_country.keys():
        by_country[country_key] = slugify(country_key)

    return render(request, 'seasons.html',
                  context={'seasons': seasons,
                           'by_country': by_country})


def get_by_country(request):
    """Gets GP per countries for seasons_page"""

    if request.method == 'POST':
        country = request.POST.get('country_name')
        tracks_per_country = []
        get_tracks_by_country = GPEvent.objects.filter(circuit__country=country).order_by('circuit__track_name')
        for gp in get_tracks_by_country:
            tracks_per_country.append(gp.circuit.track_name)
        tracks_per_country = list(dict.fromkeys(tracks_per_country))
        gp_for_country = {}
        for track in tracks_per_country:
            gp_for_country[track] = serializers.serialize("json", GPEvent.objects.filter(circuit=track).order_by('year__year'))
        response = json.dumps(gp_for_country, indent=2)

    return JsonResponse(response, safe=False)


def calendar_page(request, year):
    """Renders a single season's calendar and championships results"""

    season_calendar = GPEvent.objects.filter(year=year)
    get_dates = []
    for events in season_calendar:
        one_session = SessionResults.objects.filter(gp_id=events.id,
                                                    session_type="Course").first()
        get_dates.append(one_session.session_date)

    get_dates.sort()

    round_number = 1
    season_schedule = {}
    for gp_date in get_dates:
        get_one_session = SessionResults.objects.filter(session_date=gp_date, session_type="Course").first()
        get_gp_event = GPEvent.objects.get(id=get_one_session.gp_id.id)
        season_schedule[round_number] = [get_gp_event.gp_name, get_gp_event.gp_slug_name, year]
        round_number += 1

    return render(request, 'year.html',
                  context={'season_year': year,
                           'season_calendar': season_schedule})


def get_standings(request):
    """Fetch standing(s) for a season"""

    if request.method == 'POST':
        year = request.POST.get('year')
        tableid = request.POST.get('tableid')
        for thing in DriverChampionshipResults.objects.filter(year=year).order_by("driver_rank"):
            print(thing.driver, thing.driver_rank)
        if tableid == "table-d-ch":
            response = serializers.serialize("json", DriverChampionshipResults.objects.filter(year=year).order_by("driver_rank"))
        elif tableid == "table-c-ch":
            response = serializers.serialize("json", TeamChampionshipResults.objects.filter(year=year).order_by("team_rank"))

    return JsonResponse(response, safe=False)


def current_year_page(request):
    """Renders current season's calendar and results"""

    date = datetime.date.today()

    d_ch_results = DriverChampionshipResults.objects.filter(year=date.year).order_by("-driver_points")
    t_ch_results = TeamChampionshipResults.objects.filter(year=date.year).order_by("-team_points")

    season_calendar = GPEvent.objects.filter(year=date.year)
    round_number = 1
    season_schedule = {}
    for query in season_calendar:
        season_schedule[round_number] = [query.gp_name, query.gp_slug_name, date.year]
        round_number += 1

    return render(request, 'current_season.html',
                  context={'season_year': date.year,
                           'season_calendar': season_schedule,
                           'd_ch_res': d_ch_results,
                           't_ch_res': t_ch_results})


def gp_results(request, year, gp_slug):
    """Renders results for a GP week-end"""

    gp_info = GPEvent.objects.get(year=year, gp_slug_name=gp_slug)

    my_gp = SessionResults.objects.filter(gp_id=gp_info)
    my_sessions = []
    for gp in my_gp:
        my_sessions.append(gp.session_type)
    my_sessions = list(dict.fromkeys(my_sessions))

    weekend_results = {}
    for session in my_sessions:
        if session == 'Qualifications':
            quali_session = SessionResults.objects.filter(gp_id=gp_info,
                                                          session_type=session)
            for stuff in quali_session:
                print(stuff.driver, stuff.end_pos)
            quali_rank = []
            rank = 1
            for quali_rslts in quali_session:
                quali_rank.append({rank: quali_rslts})
                rank += 1
            weekend_results[session] = quali_rank
        else:
            weekend_results[session] = SessionResults.objects.filter(gp_id=gp_info,
                                                                     session_type=session).order_by("end_pos")
    current_year = datetime.date.today().year

    return render(request, 'grandprix.html',
                  context={'weekend_results': weekend_results,
                           'gp_info': gp_info,
                           'current_year': current_year})


@ensure_csrf_cookie
def driver_page(request):
    """Renders drivers list page"""

    return render(request, 'drivers.html',
                  context={'letters': list(string.ascii_uppercase)})


def get_driver(request):
    """"Fetch driver data for driver_page"""

    if request.method == 'POST':
        letter = request.POST.get('letter')
        drivers_for_letter = Driver.objects.filter(last_name__istartswith=letter).order_by("last_name")
        response = serializers.serialize("json", drivers_for_letter)

    return JsonResponse(response, safe=False)


def driver_info(request, driver_slug):
    """Renders driver info page"""

    my_driver = Driver.objects.get(slug_name=driver_slug)
    driver_rslts = SessionResults.objects.filter(driver=my_driver,
                                                 session_type='Course').order_by('session_date')

    driver_podium_rslts = SessionResults.objects.filter(driver=my_driver,
                                                     session_type='Course', end_pos__range=(1, 3)).order_by('end_pos')

    driver_win_rslts = SessionResults.objects.filter(driver=my_driver,
                                                        session_type='Course', end_pos=1)

    driver_ch_rslts = DriverChampionshipResults.objects.filter(driver=my_driver, driver_rank=1).order_by('year')

    driver_standings = DriverChampionshipResults.objects.filter(driver=my_driver)

    return render(request, 'driver_page.html',
                  context={'driver_profile': my_driver,
                           'driver_rslts': driver_rslts,
                           'driver_podium_rslts': driver_podium_rslts,
                           'driver_win_rslts': driver_win_rslts,
                           'driver_ch_rslts': driver_ch_rslts,
                           'driver_standings': driver_standings})


def search_results(request):
    """Renders search results page"""

    results = []
    if request.method == "GET":
        query = request.GET.get("q")
        if query is None:
            results = None
        else:
            if bool(re.search(r'\d', query)) is True:
                nb_search = ""
                nb_search = nb_search.join(re.findall(r'\d', query))
                query = query.replace(nb_search, "").strip()
                nb_search = int(nb_search)
                gp_filter_by_name = GPEvent.objects.filter(year=nb_search, gp_name__icontains=query)
                gp_filter_by_track = GPEvent.objects.filter(year=nb_search, circuit__track_name__icontains=query)
                championship_filter = ChampionshipYear.objects.filter(year=nb_search)
                results.append({"gp_query": [gp_filter_by_name, gp_filter_by_track]})
                results.append({"championship_query": championship_filter})
            else:
                driver_filter = Driver.objects.filter(full_name__icontains=query)
                gp_filter_by_name = GPEvent.objects.filter(gp_name__icontains=query).order_by("year")
                gp_filter_by_track = GPEvent.objects.filter(circuit__track_name__icontains=query).order_by("year")
                results.append({"driver_query": driver_filter})
                results.append({"gp_query": [gp_filter_by_name, gp_filter_by_track]})

    return render(request, 'search.html',
                  context={'results': results})