from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm 

app = Flask(__name__)
app.config['SECRET_KEY'] = '28073200c4225f16fc62263413475c92'

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "user" and form.password.data == "pass":
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template("login.html", form=form)

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template("register.html", form=form)

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True) 
