from flask import Flask, render_template, url_for, flash, redirect, request
from donationTracker import app, db, bcrypt
from donationTracker.models import User, Location, Item
from donationTracker.forms import RegistrationForm, LoginForm, LocationForm, ItemForm, CategorySearch, ItemSearch
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
@login_required
def dashboard():
    return redirect(url_for('category_search'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route('/locations')
@login_required
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/<int:location_id>')
@login_required
def location(location_id):
    location = Location.query.get_or_404(location_id)
    items = Item.query.filter_by(location_id=location.id).all()
    return render_template('location.html', title=location.name, location=location, items=items)

@app.route('/locations/new', methods=["GET","POST"])
@login_required
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(name=form.name.data, lat=form.lat.data, long=form.long.data,
        address=form.address.data, city=form.city.data, state=form.state.data, zip=form.zip.data,
        type=form.type.data, phone=form.phone.data, website=form.website.data)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('create_location.html', title="New Location", form=form)

@app.route('/location/<int:location_id>/add_item', methods=["GET","POST"])
@login_required
def add_item(location_id):
    location = Location.query.get_or_404(location_id)
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data, category=form.category.data, location_id=location_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('location', location_id=location.id))
    return render_template('add_item.html', title="Add Item", form=form, location=location, legend="Add Item")

@app.route('/item/<int:item_id>/update_item', methods=["GET","POST"])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    location = Location.query.get_or_404(item.location_id)
    if current_user.user_type != 'location_employee':
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category = form.category.data
        db.session.commit()
        return redirect(url_for('item', item_id=item.id))
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.category.data = item.category
    return render_template('add_item.html', title="Update Item", form=form, location=location, legend="Update Item")

@app.route('/item/<int:item_id>/delete_item', methods=["POST"])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    location = Location.query.get_or_404(item.location_id)
    if current_user.user_type != 'location_employee':
        abort(403)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('location', location_id=location.id))

@app.route('/item/<int:item_id>')
@login_required
def item(item_id):
    item = Item.query.get_or_404(item_id)
    location = Location.query.get_or_404(item.location_id)
    return render_template('item.html', title=item.name, item=item, location=location)

@app.route('/dashboard/category_search', methods=["GET","POST"])
@login_required
def category_search():
    form = CategorySearch()
    items = []
    if form.validate_on_submit():
        if form.locations.data == 'all':
            items = Item.query.filter_by(category=form.category.data).all()
        else:
            location = Location.query.get(int(form.locations.data))
            items = []
            for item in location.items:
                if item.category == form.category.data:
                    items.append(item)
    return render_template('category_search.html', title='Dashboard',form=form, items=items)

@app.route('/dashboard/item_search', methods=["GET","POST"])
@login_required
def item_search():
    form = ItemSearch()
    items = []
    if form.validate_on_submit():
        if form.locations.data == 'all':
            items = Item.query.filter_by(name=form.name.data).all()
        else:
            location = Location.query.get(int(form.locations.data))
            items = []
            for item in location.items:
                if item.name == form.name.data:
                    items.append(item)
    return render_template('item_search.html', title='Dashboard', form=form, items=items)
