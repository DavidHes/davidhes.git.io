from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from forms import FirmenRegistrierungsForm, AnmeldeFormular, KundenRegistrierungsForm, Angebotkaufen, AngebotsFormular, BewertungsFormular, Needforregistration
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

@app.route('/ratenow')
def ratenow():
     form = BewertungsFormular()
     return render_template('rating_form.html', condition=condition, form=form)

@app.route('/home')
def home():
    return render_template('home.html', condition=condition)

@app.route('/profil')
def profil():
     return render_template('profil.html', condition=condition)

#wenn der kunde bei angebot details auf jetztkaufen klickt.
@app.route('/Jetztkaufen')
def checkregistration(key):
     
     if condition:
          return redirect(url_for('buyoffernow', key=key))
     else:
         return redirect(url_for('needforregistration'))
     
#3abed screen mit registrierungsmöglichkeiten
@app.route('/Registernow', methods=['GET', 'POST'])
def needforregistration():
     form = Needforregistration()

     if request.method == 'POST' and form.validate_on_submit():
        if form.BäckereiRegistierung.data:
            return redirect(url_for('register_company'))
        elif form.Kundenregistierung.data:
            return redirect(url_for('register_customer'))
     else:
        return render_template('Needforregistration.html', form=form)


@app.route('/browse')
def browse():
    # Text "Hallo" in Firebase speichern

    ref = db.reference('offers')  # Annahme: 'offers' ist der Pfad in der Firebase-Datenbank
    offers = ref.get()  # Holen der Angebote

    if not offers:
        offers = []

    print(offers)
    return render_template('browse.html', offers=offers)

   # ref = db.reference('messages')
   # ref.push('was')
    #flash('Text "Hallo" gespeichert!', 'success')
    #return render_template('browse.html')

@app.route('/angebot/<key>')
def angebot_details(key):

    ref = db.reference('offers')  # Annahme: 'offers' ist der Pfad in der Firebase-Datenbank
    offers = ref.get()  # Holen der Angebote

    if key in offers:
        offer = offers[key]
        return render_template('angebot_details.html', offer=offer)
    else:
        return "Angebot nicht gefunden", 404

#screen mit angebot und paypal, form vllt nicht nötig.   
@app.route('/angebot/<key>/<int:id>')
def buyoffernow(key, id):
    form= Angebotkaufen()
    key = request.args.get('key')
    ref = db.reference('offers')  # Annahme: 'offers' ist der Pfad in der Firebase-Datenbank
    offers = ref.get()  # Holen der Angebote

    if key in offers:
        offer = offers[key]
        return render_template('buyoffernow.html', offer=offer, form=form)
    else:
        return "Angebot nicht gefunden", 404
    
@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = FirmenRegistrierungsForm()
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
    form = KundenRegistrierungsForm()
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
    form = AngebotsFormular()
    if form.validate_on_submit():
        # Hier könnten Sie die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Offer successfully created!', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite nach erfolgreicher Erstellung des Angebots

    return render_template('offer_form.html', form=form)

@app.route('/rate_product', methods=['GET', 'POST'])
def rate_product():
    form = BewertungsFormular()
    if form.validate_on_submit():
        # Hier könnten Sie die Daten verarbeiten, z.B. in der Datenbank speichern
        flash('Rating successfully submitted!', 'success')
        return redirect(url_for('index'))  # Beispiel: Weiterleitung zur Startseite nach erfolgreicher Bewertung
    return render_template('rating_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AnmeldeFormular()
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
