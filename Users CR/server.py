from flask import Flask, render_template, redirect, request
from user import User

app = Flask(__name__)

@app.route("/")
def index():
    # call the get all classmethod to get all friends
    users = User.get_all_users()
    print(users)
    return render_template("read.html", all_users = users)



@app.route("/add_user")
def add_user():
    return render_template("create.html")


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
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
