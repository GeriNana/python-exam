from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_data = {'id': session['user_id']}
        logged_user = User.get_user_by_id(user_data)
        sightings = Sighting.get_all()
        print("Fetched sightings:", sightings)  # Debugging statement
        return render_template('dashboard.html', sightings=sightings, logged_user=logged_user)
    return redirect('/')

@app.route('/sightings/new')
def new_sighting():
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        logged_user = User.get_user_by_id(user_data)
        return render_template('addSighting.html', logged_user=logged_user)
    return redirect('/')

@app.route('/sighting', methods=['POST'])
def create_sighting():
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect(request.referrer)
    data = {
        'location': request.form['location'],
        'description': request.form['description'],
        'date_of_sighting': request.form['date_of_sighting'],
        'number_of_sasquatches': request.form['number_of_sasquatches'],
        'user_id': session['user_id']
    }
    Sighting.create(data)
    return redirect('/dashboard')

@app.route('/sighting/edit/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    sighting = Sighting.get_sighting_by_id(data)
    if sighting and sighting['user_id'] == session['user_id']:
        user_data = {
            'id': session['user_id']
        }
        logged_user = User.get_user_by_id(user_data)
        return render_template('editSighting.html', sighting=sighting, logged_user=logged_user)
    return redirect('/dashboard')

@app.route('/sighting/update/<int:id>', methods=['POST'])
def update_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect(request.referrer)
    data = {
        'id': id,
        'location': request.form['location'],
        'description': request.form['description'],
        'date_of_sighting': request.form['date_of_sighting'],
        'number_of_sasquatches': request.form['number_of_sasquatches']
    }
    Sighting.update(data)
    return redirect('/dashboard')

@app.route('/sighting/<int:id>')
def view_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    sighting = Sighting.get_sighting_by_id(data)
    if sighting:
        usersWhoLikes = Sighting.get_users_who_liked_by_sighting_id({'sighting_id': id})
        user_data = {'id': session['user_id']}
        logged_user = User.get_user_by_id(user_data)
        user_liked = any(user['id'] == logged_user.id for user in usersWhoLikes)
        return render_template('sighting.html', sighting=sighting, usersWhoLikes=usersWhoLikes, logged_user=logged_user, user_liked=user_liked)
    return redirect('/dashboard')

@app.route('/sighting/delete/<int:id>', methods=['POST'])
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    Sighting.delete(data)
    return redirect('/dashboard')


@app.route('/add/like/<int:id>', methods=['POST'])
def add_like(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sighting_id': id,
        'user_id': session['user_id']
    }
    Sighting.add_like(data)
    return redirect('/sighting/' + str(id))

@app.route('/remove/like/<int:id>', methods=['POST'])
def remove_like(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sighting_id': id,
        'user_id': session['user_id']
    }
    Sighting.remove_like(data)
    return redirect('/sighting/' + str(id))