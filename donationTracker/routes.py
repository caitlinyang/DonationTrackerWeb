from flask import Flask, render_template, url_for, flash, redirect, request
from donationTracker import app, db, bcrypt
from donationTracker.models import User, Location, Item
from donationTracker.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template("login.html", form=form)


@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in.','success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", title="Dashboard")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/<int:location_id>')
def location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location.html', title=location.name, location=location)
