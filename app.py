from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_bootstrap import Bootstrap5
import forms

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
)
bootstrap = Bootstrap5(app)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/favourites/')
def favourites():
     return render_template('favourite.html')

@app.route('/profil/')
def favourites():
     return render_template('profil.html')
   
@app.route('/browse/')
def browse():
    return render_template('browse.html')

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = forms.CompanyregistrationForm()
    if form.validate_on_submit():
        # Hier kannst du die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Company successfully registered!', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite
    return render_template('company_registration_form.html', form=form)

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = forms.CustomerregistrationForm()
    if form.validate_on_submit():
        # Hier könnten Sie die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Customer successfully registered!', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite nach erfolgreicher Registrierung

    return render_template('customer_registration_form.html', form=form)

@app.route('/create_offer', methods=['GET', 'POST'])
def create_offer():
    form = forms.OfferForm()
    if form.validate_on_submit():
        # Hier könnten Sie die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Offer successfully created!', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite nach erfolgreicher Erstellung des Angebots

    return render_template('offer_creation_form.html', form=form)

@app.route('/rate_product', methods=['GET', 'POST'])
def rate_product():
    form = forms.RatingForm()
    if form.validate_on_submit():
        # Hier könnten Sie die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Rating successfully submitted!', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite nach erfolgreicher Bewertung
    return render_template('rating_form.html', form=form)

@app.route('/login_Form', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        
        #SICHER PASSWÖRTE SPEICHERN
        #from werkzeug.security import generate_password_hash, check_password_hash
        #Passwort hashen
        #password = "mypassword123"
        #hashed_password = generate_password_hash(password, method='sha256')

        # Hier könnten Sie die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Logged in successfully', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite nach erfolgreicher Bewertung
    return render_template('login_form.html', form=form)