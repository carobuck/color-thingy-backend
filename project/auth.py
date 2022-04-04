from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
#from . import db

import config
cred = credentials.Certificate(config.firestore_secret)
firebase_admin.initialize_app(cred)
db_fs = firestore.client()

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')



# https://cloud.google.com/community/tutorials/using-flask-login-with-cloud-datastore
@page.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        identity = request.form.get('email')
        password = request.form.get('password')

        # fetch user using the 'username' property
        # refer to the datastore-entity documentation for more
        user = User().get_obj('email',identity)

        if user and user.authenticated(password):

            if login_user(user, remember=True):
                user.update_activity()

                #handle optionally redirecting to the next URL safely
                #next_url = form.next.data
                #if next_url:
                #    return redirect(safe_next_url(next_url))

            #    return redirect(url_for('page/dashboard.html'))
            else:
                flash('This account is not active','error')

        else:
            flash('Login or password is incorrect','error')
            return redirect(url_for('auth.login'))

    return redirect(url_for('main.profile'))



@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # TODO: convert database to using firebase?? (unless can deploy to app engine w/o committing db.sqlite...?)
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
