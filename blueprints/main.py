from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from ..models.person import Person
from ..extensions import db

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/edit')
def edit_profile():
    user = Person.query.filter_by(id=current_user.id).first()
    if user is None:
        flash('User not found')
        return redirect('/')
    data = user.to_dict()
    return render_template('edit_profile.html', data=data)


@main.route('/edit', methods=['POST'])
def edit_profile_post():
    user = Person.query.filter_by(id=current_user.id).first()
    if user is None:
        flash('User not found')
        return redirect('/')

    if request.form['email'] != '':
        user.email = request.form['email']

    if request.form['name'] != '':
        user.name = request.form['name']

    if request.form['password'] != '':
        password = request.form['password']
        user.password = generate_password_hash(password)

    print(user.email, user.name, user.password)
    db.session.commit()
    logout_user()
    login_user(user)
    return redirect(url_for('main.profile'))


@main.route('/remove')
@login_required
def remove():
    user = Person.query.filter_by(id=current_user.id).first()
    print(user)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        flash('User not found')
        return redirect(url_for('main.profile'))


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
