from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models.person import Person

auth = Blueprint('auth', __name__,
                 template_folder='templates')


@auth.route('/login')
def do_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def do_login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember_me = request.form.get('remember_me')

    user_exists = Person.query.filter_by(email=email).first()
    if not user_exists:
        flash('Email or password is incorrect')
        return redirect(url_for('auth.do_login'))
    if check_password_hash(user_exists.password, password):
        login_user(user_exists, remember=remember_me)
        return redirect(url_for('main.profile'))
    else:
        flash('Email or password is incorrect')
        return redirect(url_for('auth.do_login'))


@auth.route('/signup', methods=['GET', 'POST'])
def do_signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user_exists = Person.query.filter_by(email=request.form['email'])

        if user_exists.count() > 0:
            flash('Email already exists')
            return redirect(url_for('auth.do_signup'))
        else:
            hashed_password = generate_password_hash(
                password=password)
            new_user = Person(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            user = Person.query.filter_by(id=new_user.id).first()
            login_user(user)
            return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def do_logout():
    logout_user()
    return redirect(url_for('main.index'))
