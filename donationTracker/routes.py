from flask import Flask, render_template, url_for, flash, redirect
from donationTracker import app
from donationTracker.models import User
from donationTracker.forms import RegistrationForm, LoginForm 

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "user" and form.password.data == "pass":
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template("login.html", form=form)

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template("register.html", form=form)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", title="Dashboard")
