from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, HiddenField, BooleanField, SelectField, DateTimeField, RadioField, IntegerField
from wtforms.validators import InputRequired, Length, Email, NumberRange

class CompanyregistrationForm(FlaskForm):
    companyname = StringField(validators=[InputRequired(), Length(min=5)])
    street = StringField(validators=[InputRequired(), Length(min=5)])
    city = StringField(validators=[InputRequired(), Length(min=5)])
    postcode = StringField(validators=[InputRequired(), Length(min=5)])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    email = EmailField(validators=[InputRequired(), Email()])
    openinghour=DateTimeField(validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    closinghour=DateTimeField(validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    terms = BooleanField(validators=[InputRequired()])
    submit = SubmitField('Create')

class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Login')

class CustomerregistrationForm(FlaskForm):
    customername = StringField(validators=[InputRequired(), Length(min=5)])
    customerfirstname  = StringField(validators=[InputRequired(), Length(min=5)])
    password = PasswordField(validators=[InputRequired(), Length(min=5)])
    email = EmailField(validators=[InputRequired(), Email()])
    submit = SubmitField('Create Account')

class OfferForm(FlaskForm):
    offerdescription = StringField(validators=[InputRequired(), Length(min=5)])
    titel = StringField(validators=[InputRequired(), Length(min=5)])
    category = SelectField(choices=['tech', 'Technology','finance', 'Finance', 'health', 'Healthcare'])
    numberofbags = IntegerField(validators=[InputRequired(), NumberRange(min=1)])
    price = IntegerField(validators=[InputRequired(), NumberRange(min=1)])
    startPickuptime=DateTimeField(validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    endPickuptime=DateTimeField(validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    dailynumberofbags = BooleanField(validators=[InputRequired()])
    terms = BooleanField(validators=[InputRequired()])
    submit = SubmitField('Create Offer')

class RatingForm(FlaskForm):
    rating = RadioField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], coerce=int, validators=[InputRequired()])
    review = StringField(Length(min=5))
    submit = SubmitField('Submit Review')
