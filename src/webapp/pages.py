from flask import Blueprint, render_template

# Initialize blueprint as pages
pages = Blueprint("pages", __name__)


# @pages decorator dictates / route renders index.html
@pages.route("/")
def home():
    return render_template("index.html")


# @pages decorator dictates /convert round renders convert.html
@pages.route("/convert")
def convert():
    return render_template("convert.html")


# @pages decorator dictates /analyze round renders analyze.html
@pages.route("/analyze")
def analyze():
    return render_template("analyze.html")


# @pages decorator dictates /analyze round renders analyze.html
@pages.route("/info")
def info():
    return render_template("info.html")
