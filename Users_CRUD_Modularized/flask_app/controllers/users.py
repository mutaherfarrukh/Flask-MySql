from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User




@app.route("/")
def index():
    # call the get all classmethod to get all friends
    users = User.get_all_users()
    print(users)
    return render_template("read.html", all_users = users)


@app.route("/add_user")
def add_user():
    return render_template("create.html")

# @app.route("/read_one")
# def read_one():
#     return render_template("edit.html")
@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the user class.
    User.save_user(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/readone.html', user =user)

@app.route('/show/<int:id>')
def show(id):
    data = {
        "id": id
    }
    # We pass the data dictionary into the save method from the user class.
    user = User.get_one_user(data)
    # Don't forget to redirect after saving to the database.
    return render_template('/readone.html', user =user)

@app.route('/edit/<int:id>')
def edit(id):
    data = {
        "id": id
    }
    # We pass the data dictionary into the save method from the user class.
    user = User.get_one_user(data)
    # Don't forget to redirect after saving to the database.
    return render_template('edit.html', user =user)

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        "id": id
    }
    # We pass the data dictionary into the save method from the user class.
    user = User.delete_user(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/')


@app.route('/update/<int:id>', methods=["POST"])
def update(id):
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string
    user = User.update_user(request.form)
    # We pass the data dictionary into the save method from the user clas
    return redirect(f"/show/{request.form['user_id']}")