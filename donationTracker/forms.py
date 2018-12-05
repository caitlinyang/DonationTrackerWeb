from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from donationTracker.models import User, Location, Item

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('user','User'),('location_employee','Location Employee'),('admin','Admin')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please pick another email.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2,max=100)])
    address = StringField('Addresss', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired(), Length(min=2,max=2)])
    zip = StringField('Zip Code', validators=[DataRequired()])
    lat = StringField('Lat', validators=[DataRequired()])
    long = StringField('Long', validators=[DataRequired()])
    type = SelectField('Type', choices=[('drop_off','Drop Off'), ('store','Store'), ('warehouse','Warehouse')])
    phone = StringField('Phone', validators=[DataRequired()])
    website = StringField('Website', validators=[DataRequired()])
    submit = SubmitField('Create Location')

    def validate_username(self, username):
        location = Location.query.filter_by(address=address.data).first()
        if location:
            raise ValidationError('No duplicate locations.')

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2,max=100)])
    description = TextAreaField('Description',validators=[DataRequired()])
    submit = SubmitField('Submit Item')
