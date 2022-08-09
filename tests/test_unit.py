from datetime import datetime

from utils import (
    book_at_least_one_place,
    book_more_places_than_allowed,
    club_has_enough_points,
    copy_file_a_to_file_b,
    is_past_competition,
    load_file,
    places_into_points,
    points_into_places,
    string_to_datetime,
    update_clubs,
    update_competitions,
)


def test_load_file():
    test_clubs = load_file("tests/files_test/test_clubs.json")
    expected_clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]

    assert test_clubs == expected_clubs


def test_update_clubs(tearDownClubs):

    list_club_before_update = load_file("tests/files_test/test_update_clubs.json")
    points_before_update = list_club_before_update[0]["points"]
    point_used = 1
    assert points_before_update == "13"

    update_list_club_by_using_one_points = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "12"}
    ]
    update_clubs(
        update_list_club_by_using_one_points, "tests/files_test/test_update_clubs.json"
    )
    test_update_clubs = load_file("tests/files_test/test_update_clubs.json")
    expected_value = str(int(points_before_update) - point_used)
    assert test_update_clubs[0]["points"] == expected_value


def test_update_competitions(tearDownCompetitions):

    list_competition_before_update = load_file(
        "tests/files_test/test_update_competitions.json"
    )
    places_before_update = list_competition_before_update[0]["places"]
    place_purchased = 1
    assert places_before_update == "25"

    update_list_competition_by_purchasing_one_place = [
        {"name": "Spring Festival", "date": "2023-03-27 10:00:00", "places": "24"}
    ]
    update_competitions(
        update_list_competition_by_purchasing_one_place,
        "tests/files_test/test_update_competitions.json",
    )
    test_update_competitions = load_file(
        "tests/files_test/test_update_competitions.json"
    )
    expected_value = str(int(places_before_update) - place_purchased)
    assert test_update_competitions[0]["places"] == expected_value


def test_club_has_enough_points():
    assert club_has_enough_points(3, 9) is True
    assert club_has_enough_points(3, 3) is True
    assert club_has_enough_points(3, 2) is False


def test_convert_points_into_places():
    assert points_into_places(3) == 1
    assert points_into_places(7) == 2


def test_convert_places_into_points():
    assert places_into_points(3) == 9


def test_convert_string_to_datetime():
    assert string_to_datetime("2023-03-27 10:00:00") == datetime(2023, 3, 27, 10, 0, 0)


def test_is_past_competition():
    assert is_past_competition(datetime(2020, 1, 24, 14, 4, 57)) is True


def test_is_future_competition():
    assert is_past_competition(datetime(2023, 1, 24, 14, 4, 57)) is False


def test_book_more_places_than_allowed():
    assert book_more_places_than_allowed(13) is True


def test_book_less_places_than_allowed():
    assert book_more_places_than_allowed(9) is False


def test_book_one_place():
    assert book_at_least_one_place(1) is True


def test_book_more_than_one_place():
    assert book_at_least_one_place(2) is True


def test_book_less_than_one_place():
    assert book_at_least_one_place(0) is False


def test_copy_file_a_to_file_b():

    expected_file_a_before_copy = load_file("tests/files_test/file_a.json")
    expected_file_b_before_copy = load_file("tests/files_test/file_b.json")

    copy_file_a_to_file_b(
        "tests/files_test/file_a.json", "tests/files_test/file_b.json"
    )

    expected_file_a_after_copy = load_file("tests/files_test/file_a.json")
    expected_file_b_after_copy = load_file("tests/files_test/file_b.json")

    assert expected_file_a_before_copy == [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    ]
    assert expected_file_a_after_copy == [
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}
    ]
    assert expected_file_b_before_copy == [
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}
    ]
    assert expected_file_b_after_copy == [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    ]

    copy_file_a_to_file_b(
        "tests/files_test/file_a.json", "tests/files_test/file_b.json"
    )
