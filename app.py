import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from scraper import get_menu

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blog.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show Menu"""
    if request.method == "POST":
        menu = request.form.get("menu")
        menu = get_menu(menu)

        return render_template("selected.html", menu=menu)
    else:
        return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Upload a review to the database."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("review"):
            return apology("missing review")
        elif not request.form.get("rating"):
            return apology("missing rating")

        username = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

        db.execute("INSERT INTO POSTS ('name', 'input', 'rating') \
                    VALUES (?, ?, ?)", username, request.form.get("review"), int(request.form.get("rating")))

        # Display Posts
        flash("Submitted!")
        return redirect("/profile")

    # GET
    else:
        return render_template("upload.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = :username", username=username):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/feed")
@login_required
def feed():
    """Displays all the posts from the database."""
    posts = db.execute("SELECT * FROM POSTS ORDER BY time DESC")
    # Gets the average score for today
    average_score = db.execute("SELECT AVG(rating) FROM POSTS WHERE time >= CURRENT_DATE")[
        0]["AVG(rating)"]
    return render_template("feed.html", posts=posts, average_score=average_score)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                            request.form.get("username"),
                            generate_password_hash(request.form.get("password")))
        except ValueError:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Displays the reviews of the user logged in."""

    # POST
    if request.method == "POST":

        # Deletes the specified post the user's profile
        post_id = request.form.get("post_id")
        db.execute("DELETE FROM POSTS WHERE post_id = ?", post_id)
        flash("Deleted!")
        return redirect("/profile")
    # GET
    else:

        # Get posts from user
        username = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        posts = db.execute(
            "SELECT time, input, rating, post_id FROM POSTS WHERE name = ? ORDER BY time DESC", username)

        average_score = db.execute(
            "SELECT AVG(rating) FROM POSTS WHERE name = ?", username)[0]["AVG(rating)"]
        # Display sales form
        return render_template("profile.html", posts=posts, average_score=average_score)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
