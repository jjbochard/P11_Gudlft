from flask import Flask, flash, redirect, render_template, request, url_for

from utils import (
    MAX_PLACES_ALLOWED_PER_COMPETITION,
    POINTS_PER_PLACE,
    book_at_least_one_place,
    book_more_places_than_allowed,
    club_has_enough_points,
    is_past_competition,
    load_file,
    places_into_points,
    points_into_places,
    string_to_datetime,
    update_clubs,
    update_competitions,
)

app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_file("competitions.json")
clubs = load_file("clubs.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/clubs")
def showClubs():
    return render_template("clubs.html", clubs=clubs)


@app.route("/showSummary", methods=["POST", "GET"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Please enter a valid secretary email")
        return redirect("/")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


@app.route("/book/<competition>/<club>", methods=["GET"])
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
        if foundClub and foundCompetition:
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
    except IndexError:
        flash("Something went wrong-please try again")
        return redirect("/", code=404)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    clubPoints = int(club["points"])
    max_places = points_into_places(clubPoints)
    pointsUsed = places_into_points(placesRequired)

    if is_past_competition(string_to_datetime(competition["date"])):
        flash("You cannot book places in past competition")
    elif not club_has_enough_points(pointsUsed, clubPoints):
        flash(f"Your club has not enough points to purchase {placesRequired} places.")
        flash(
            f"You can purchase {max_places} place(s) maximum. ({POINTS_PER_PLACE} points per place)"
        )
    elif book_more_places_than_allowed(placesRequired):
        flash(
            f"You cannot book more than {MAX_PLACES_ALLOWED_PER_COMPETITION} places per competition"
        )
    elif not book_at_least_one_place(placesRequired):
        flash("You cannot book less than one place")
    else:
        competition["numberOfPlaces"] = str(
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club["points"] = str(int(club["points"]) - pointsUsed)
        update_clubs(clubs, "clubs.json")
        update_competitions(competitions, "competitions.json")
        flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
