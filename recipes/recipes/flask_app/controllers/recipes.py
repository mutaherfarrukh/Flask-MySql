from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash

########################
# careate car route
# ########################
# @app.route("/new_recipe")
# def new_recipe():
#     if not "user_id" in session:
#         flash('Please login before using our site!')
#         return redirect('/')

#     return render_template("/new_recipe.html")




@app.route("/")
def get_all_recipes():
    # call the get all classmethod to get all friends
    recipes = Recipe.get_all_recipes()

    return render_template("dashboard.html", all_recipes = recipes)


@app.route('/recipes/<int:id>')
def recipe(id):
    data = {
        "id": id
    }
    # We pass the data dictionary into the save method from the user class.
    recipe = Recipe.get_recipe_info(data)
    # Don't forget to redirect after saving to the database.
    return render_template('/recipes.html', recipe =recipe)


@app.route("/recipe/new")
def add_recipe():
    return render_template("create.html")


@app.route("/create_recipe", methods=['POST'])
def create_recipe():
    print('hellocreate')
    if not Recipe.validate_recipe(request.form):
        return redirect('/create_recipe')

    user_id = session['user_id']
    data = {

        'description': request.form['description'],
        'name': request.form['name'],
        'instruction': request.form['instruction'],
        'under30min': request.form['under30min'],
        # 'updated_at': request.form['updated_at'],
        "user_id": user_id
    }
    Recipe.save_recipe(data)
    return redirect('/dashboard')


# @app.route("/dashboard")
# def back_to_dashboard():
#     return render_template("recipes.html")

##################################
###EDIT
#################################

@app.route('/update/<int:id>', methods=["POST"])
def update(id):
    data ={
    'id' : id, 
    'name' : request.form['name'],
    'description' : request.form['description'],
    'instruction' : request.form['instruction'],
    'under30min' : request.form['under30min'],
    }

    recipe = Recipe.update_recipe(data)
    # We pass the data dictionary into the save method from the user clas
    
    return redirect(f"/dashboard")



@app.route('/recipe/edit/<int:recipe_id>')
def edit(recipe_id):
    if not 'user_id' in session:
        flash('Please login before using the site')
        return redirect('/')
    data = {
        "id": recipe_id
    }
    one_recipe = Recipe.get_recipe_info(data)
    logged_user_id = session['user_id']
    # We pass the data dictionary into the save method from the user class.
    # recipe = Recipe.get_one_recipe(data)
    
    if logged_user_id != session['user_id']:
        flash('You ara not authorized to use this page!')
        return redirect('/dashboard')
    # Don't forget to redirect after saving to the database.
    return render_template('edit.html', one_recipe =one_recipe, user_id =logged_user_id)



@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if not 'user_id' in session:
        flash("Please login before using our side ")
        return redirect('/')

    data = {
        'id': recipe_id
    }

    Recipe.eliminate_recipe(data)
    return redirect("/dashboard")


