import json
from datetime import datetime

MAX_PLACES_ALLOWED_PER_COMPETITION = 12
POINTS_PER_PLACE = 3


def load_file(file):
    with open(file) as f:
        return json.load(f)


def update_clubs(list_clubs, file_to_update):
    with open(file_to_update, "w") as c:
        json.dump(list_clubs, c, indent=4)


def update_competitions(list_competition, file_to_update):
    with open(file_to_update, "w") as c:
        json.dump(list_competition, c, indent=4)


def points_into_places(points):
    return points // POINTS_PER_PLACE


def places_into_points(places):
    return places * POINTS_PER_PLACE


def club_has_enough_points(points_used, clubs_points):
    return points_used <= clubs_points


def string_to_datetime(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def is_past_competition(competition_date):
    return datetime.now() > competition_date


def book_more_places_than_allowed(places):
    return places > MAX_PLACES_ALLOWED_PER_COMPETITION


def book_at_least_one_place(places):
    return places >= 1


def copy_file_a_to_file_b(file_a, file_b):
    with open(file_a, "r") as openfile:
        a = json.load(openfile)
    with open(file_b, "r") as openfile:
        b = json.load(openfile)

    update_clubs(a, file_b)
    update_clubs(b, file_a)
