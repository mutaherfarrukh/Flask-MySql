import re
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def login_reg():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save_user(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

#########################################################
# login route
#########################################################


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database

    data = {"email": request.form["email"]}

    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

    #######################################################################
    # dashboard
    #######################################################################


@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        flash("You have to login before using the site!")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_user(data)
    all_recipes = Recipe.all_recipes()
    return render_template("dashboard.html", all_recipes = all_recipes, user= user)

###############################################################
# # logout
###############################################################


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
