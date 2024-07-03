from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_bootstrap import Bootstrap5
import forms 

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
)
bootstrap = Bootstrap5(app)
condition = False

@app.route('/favourites')
def favourites():
     return render_template('favourite.html', condition=condition)

@app.route('/home')
def home():
    return render_template('home.html', condition=condition)

@app.route('/profil')
def profil():
     return render_template('profil.html', condition=condition)
   
@app.route('/browse')
def browse():
    return render_template('browse.html', condition=condition)

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = forms.CompanyregistrationForm()
    if request.method == 'GET':
        return render_template('company_registration_form.html', form=form)
    else:  # request.method == 'POST'
        if form.validate_on_submit():
            flash('Company has been registered.', 'success')
            return redirect(url_for('profil'))
        else:
            flash('No company registration: validation error.', 'warning')
            return render_template('company_registration_form.html', form=form)

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = forms.CustomerregistrationForm()
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