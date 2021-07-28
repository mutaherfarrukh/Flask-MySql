from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.car import Car


########################
# careate car route
########################
@app.route("/new_car")
def new_car():
    if not "user_id" in session:
        flash('Please login before using our site!')
        return redirect('/')

    return render_template("/new_car.html")


@app.route("/create_car", methods=['POST'])
def create_car():

    if not Car.validate_car(request.form):
        return redirect('/new_car')

    driver_id = session['user_id']
    data = {
        'color': request.form['color'],
        'seats': request.form['seats'],
        "driver_id": driver_id
    }
    Car.save_car(data)
    return redirect('/dashboard')

####################
# show One Car route
###################


@app.route("/show_car/<int:car_id>")
def show_car(car_id):
    if not 'user_id' in session:
        flash("Please login before using our side ")
        return redirect('/')

    data = {
        'id': car_id
    }
    one_car = Car.get_car_info(data)

    return render_template('show_car.html', one_car=one_car)

#########################
# edit route
###############


@app.route('/edit_car/<int:car_id>')
def edit_car(car_id):
    if not 'user_id' in session:
        flash("Please login before using our side ")
        return redirect('/')
    data = {
        "id": car_id
    }
    one_car = Car.get_car_info(data)
    logged_user_id = session['user_id']

    if logged_user_id != one_car.user_id:
        flash('You cannot access that page!')
        return redirect('/dashboard')

    return render_template('edit_car.html', one_car=one_car, user_id=logged_user_id)


@app.route('/update_car/<int:car_id>', methods=['POST'])
def updated_car(car_id):

    if not Car.validate_car(request.form):
        return redirect(f"/edit_car/{car_id}")

    data = {
        "id": car_id,
        "color": request.form['color'],
        'seats': request.form['seats'],
    }
    Car.update_car(data)

    return redirect('/dashboard')

#########################
# delete
#########################


@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    if not 'user_id' in session:
        flash("Please login before using our side ")
        return redirect('/')

    data = {
        'id': car_id
    }

    Car.eliminate_car(data)
    return redirect("/dashboard")
