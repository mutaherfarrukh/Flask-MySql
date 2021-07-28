from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.openmic import Openmic
from flask import flash


@app.route('/openmics/create')
def create_openmic():
    if not "user_id" in session:
        flash("You have to login before using the site!")
        return redirect('/')

    user_id = session['user_id']
    return render_template('add_openmic.html', user_id=user_id)



@app.route('/add_openmic', methods=['POST'])
def add_openmic():
    if not Openmic.validate_openmic(request.form):
        # need to redirect to exact same page, not to register not dashboard
        return redirect("/openmics/create")  # return redirect to 1.i

        # now need to pull information to put data:
    data = {  # 1.iv pull data and safe after validation...
        "venue": request.form['venue'],
        "type": request.form["type"],
        "date": request.form["date"],
        "description": request.form["description"],
        "user_id": session['user_id']
        # with the above  data we need to call on  openmic as below
    }
    Openmic.save(data)  # after this need to add save methode (@@) on model

    return redirect('/dashboard')


@app.route('/openmics/edit/<int:id>')
def edit_one(id):
    if not "user_id" in session:
        flash("You have to login before using the site!")
        return redirect('/')
    # to putll the data query is needed here to open at edit_openmic.html
    data = {
        'id': id
    }
    openmic = Openmic.one_openmic(data)

    return render_template('edit_openmic.html', openmic=openmic)


@app.route("/update_openmic/<int:id>", methods=['POST'])
def update_openmic(id):
    if not Openmic.validate_openmic(request.form):
        # need to redirect to exact same page, not to register not dashboard
        return redirect(f"/openmics/edit/{id}")

    data = {
        "venue": request.form['venue'],
        "type": request.form["type"],
        "date": request.form["date"],
        "description": request.form["description"],
        "id": id,
    }
    Openmic.update_one_openmic(data)
    return redirect('/dashboard')


# @app.route("/")
# def get_all_openmics():
#     openmics = Openmic.get_all_openmics()
#     return render_template("dashboard.html", all_openmics = openmics)
