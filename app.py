from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from forms import CompanyregistrationForm, LoginForm, CustomerregistrationForm
from my_firebase_admin import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    # Text "Hallo" in Firebase speichern
    ref = db.reference('messages')
    ref.push('was')

    flash('Text "Hallo" gespeichert!', 'success')
    return render_template('browse.html')

@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = CompanyregistrationForm()
    if form.validate_on_submit():
        print('Form validated successfully!')
        
        company_data = {
            'companyname': form.companyname.data,
            'street': form.street.data,
            'city': form.city.data,
            'postcode': form.postcode.data,
            'password': generate_password_hash(form.password.data),
            'email': form.email.data,
            'openinghour': form.openinghour.data.strftime('%Y-%m-%dT%H:%M'),
            'closinghour': form.closinghour.data.strftime('%Y-%m-%dT%H:%M'),
            'terms': form.terms.data
        }
        
        # Speichern der Daten in Firebase
        ref = db.reference('companies')
        ref.push(company_data)
        
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    else:
        print('Form validation failed!')
    
    return render_template('company_registration_form.html', form=form)
    
@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = CustomerregistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        customer_data = {
            'customername': form.customername.data,
            'customerfirstname': form.customerfirstname.data,
            'email': form.email.data,
            'password': hashed_password
        }
        ref = db.reference('customers')
        ref.push(customer_data)
        flash('Customer registration successful!', 'success')
        return redirect(url_for('login'))
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ref = db.reference('customers')
        users = ref.order_by_child('email').equal_to(form.email.data).get()
        user = None
        for key, value in users.items():
            user = value
            user['id'] = key
        if user and check_password_hash(user['password'], form.password.data):
            session['user_id'] = user['id']
            flash('Logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))
