import json
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

MAX_PLACES_ALLOWED_PER_COMPETITION = 12


def loadFile(file):
    with open(file) as f:
        return json.load(f)


def updateClubs(list_clubs, file_to_update):
    with open(file_to_update, "w") as c:
        json.dump(list_clubs, c, indent=4)


def updateCompetitions(list_competition, file_to_update):
    with open(file_to_update, "w") as c:
        json.dump(list_competition, c, indent=4)


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadFile("competitions.json")
clubs = loadFile("clubs.json")


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    flash("Something went wrong-please try again")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    clubPoints = int(club["points"])

    if datetime.now() > datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S"):
        flash("You cannot book places in past competition")
    elif placesRequired > clubPoints:
        flash(f"You cannot use more than your club points ({club['points']})")
    elif placesRequired > MAX_PLACES_ALLOWED_PER_COMPETITION:
        flash(
            f"You cannot book more than {MAX_PLACES_ALLOWED_PER_COMPETITION} places per competiton"
        )
    else:
        competition["numberOfPlaces"] = str(
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club["points"] = str(int(club["points"]) - placesRequired)
        updateClubs(clubs, "clubs.json")
        updateCompetitions(competitions, "competitions.json")
        flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
