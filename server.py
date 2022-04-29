import json

from flask import Flask, flash, redirect, render_template, request, url_for

MAX_PLACES_ALLOWED_PER_COMPETITION = 12


def loadClubs():
    with open("clubs.json") as c:
        return json.load(c)["clubs"]


def loadCompetitions():
    with open("competitions.json") as comps:
        return json.load(comps)["competitions"]


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


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
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    flash("Something went wrong-please try again")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    clubPoints = int(club["points"])
    if placesRequired > clubPoints:
        flash(f"You cannot use more than your club points ({club['points']})")
    elif placesRequired > MAX_PLACES_ALLOWED_PER_COMPETITION:
        flash(
            f"You cannot book more than {MAX_PLACES_ALLOWED_PER_COMPETITION} places per competiton"
        )
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
