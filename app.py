from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bootstrap import Bootstrap5
from forms import FirmenRegistrierungsForm, AnmeldeFormular, KundenRegistrierungsForm, AngebotsFormular, BewertungsFormular, Angebotkaufen
from my_firebase_admin import db, auth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
import paypalrestsdk


app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='journal'
)
bootstrap = Bootstrap5(app)
condition = False

# PayPal configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AUJPGXC_Q2irXahFthN6EpW2PAW6E-Seh_j1AEcGpDcsbNlL8oyCWJaQ06D4-ourzL3qrOx7pifp6Zj9",
    "client_secret": "EHn6JQE0eJ-EfOflg8w1E4ogCDJrSPgcqnir2PvB_0DgpYh5L7y4G6q8Doi1fsPaXf9CJeYxO8nJw7kW"
})

@app.route('/firebase_auth_and_register', methods=['POST'])
def firebase_auth_and_register():
    data = request.get_json()  # POST-Anfrage wird an die Route /sessionLogin gesendet von login.html. Die sind immer JSON-Daten. In dem Fall idToken, name und email.
    id_token = data.get('idToken')
    name = data.get('name')
    email = data.get('email')

    try:
        decoded_token = auth.verify_id_token(id_token)
        firebase_uid = decoded_token['uid']

        # Überprüfe, ob der Benutzer bereits existiert
        ref = db.reference('customers')
        existing_users = ref.order_by_child('email').equal_to(email).get()

        user_id = None
        if not existing_users:
            # Wenn der Benutzer nicht existiert, speichere die Benutzerdaten
            customer_data = {
                'customerFirstName': name.split()[0],  # Vorname
                'customername': name,  # Ganzer Name
                'email': email,
                'firebase_uid': firebase_uid,
                'is_company': False
            }
            new_user_ref = ref.push(customer_data)
            user_id = new_user_ref.key
        else:
            # Benutzer existiert bereits, hole die benutzerdefinierte User-ID
            for key, value in existing_users.items():
                user_id = key

        # Speichere die Benutzerinformationen in der Session
        session['user_id'] = user_id  # benutzerdefinierte User-ID
        session['user_name'] = name
        session['is_company'] = False

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/favourites')
def favourites():
    return render_template('favourite.html', condition=condition)

@app.route('/home')
def home():
    user_id = session.get('user_id')
    user_name = "Gast"
    user_type = session.get('is_company')

    if user_id:
        if user_type:
            ref = db.reference(f'companies/{user_id}')
            user_data = ref.get()
        else:
            ref = db.reference(f'customers/{user_id}')
            user_data = ref.get()

        if user_data:
            user_name = user_data.get('customername' if not user_type else 'companyname', "Gast")

    return render_template('home.html', user_name=user_name, user_id=user_id)

@app.route('/profil')
def profil():
    return render_template('profil.html', condition=condition)

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
        return render_template('angebot_details.html', offer=offer, key=key)
    else:
        return "Angebot nicht gefunden", 404
    
@app.route('/Jetztkaufen/<key>')
def checkregistration(key):
    user_id = session.get('user_id')
    if user_id:
        return redirect(url_for('offer', key=key))
    else:
        return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    customer_form = KundenRegistrierungsForm(prefix='customer')
    company_form = FirmenRegistrierungsForm(prefix='company')

    if request.method == 'POST':
        if customer_form.validate_on_submit():
            print("Handling customer registration...")
            ref = db.reference('customers')
            existing_users = ref.order_by_child('email').equal_to(customer_form.email.data).get()

            if existing_users:
                flash('Email already registered. Please log in.', 'danger')
                return redirect(url_for('login'))

            customer_data = {
                'customerFirstName': customer_form.kundenVorname.data,
                'customername': customer_form.kundenname.data,
                'email': customer_form.email.data,
                'password': generate_password_hash(customer_form.passwort.data),
                'is_company': False
            }

            ref.push(customer_data)
            flash('Customer registration successful!', 'success')
            return redirect(url_for('login'))

        elif company_form.validate_on_submit():
            print("Handling company registration...")
            ref = db.reference('companies')
            existing_users = ref.order_by_child('email').equal_to(company_form.email.data).get()

            if existing_users:
                flash('Email already registered. Please log in.', 'danger')
                return redirect(url_for('login'))

            company_data = {
                'companyname': company_form.firmenname.data,
                'street': company_form.strasse.data,
                'number': company_form.hausnummer.data,
                'city': company_form.stadt.data,
                'postcode': company_form.postleitzahl.data,
                'password': generate_password_hash(company_form.passwort.data),
                'email': company_form.email.data,
                'openinghour': company_form.öffnungszeit.data.strftime('%Y-%m-%dT%H:%M'),
                'closinghour': company_form.schließzeit.data.strftime('%Y-%m-%dT%H:%M'),
                'terms': company_form.agb.data
            }

            ref.push(company_data)
            flash('Company registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('registration_form.html', customer_form=customer_form, company_form=company_form)

@app.route('/create_offer', methods=['GET', 'POST'])
def create_offer():
    form = AngebotsFormular()
    if form.validate_on_submit():
        offer_data = {
            'angebotsbeschreibung': form.angebotsbeschreibung.data,
            'titel': form.titel.data,
            'kategorie': form.kategorie.data,
            'anzahlTaschen': form.anzahlTaschen.data,
            'preis': form.preis.data,
            'abholStartZeit': form.abholStartZeit.data.strftime('%Y-%m-%dT%H:%M'),
            'abholEndZeit': form.abholEndZeit.data.strftime('%Y-%m-%dT%H:%M'),
            'täglicheAnzahlTaschen': form.täglicheAnzahlTaschen.data,
            'agb': form.agb.data
        }

        ref = db.reference('offers')
        ref.push(offer_data)

        flash('Offer successfully created!', 'success')
        return redirect(url_for('home'))

    return render_template('offer_form.html', form=form)

@app.route('/edit_offer/<offer_id>', methods=['GET', 'POST'])
def edit_offer(offer_id):
    ref = db.reference(f'offers/{offer_id}')
    offer_data = ref.get()

    if not offer_data:
        flash('Angebot nicht gefunden!', 'danger')
        return redirect(url_for('home'))

    form = AngebotsFormular(data=offer_data)
    if form.validate_on_submit():
        updated_offer_data = {
            'angebotsbeschreibung': form.angebotsbeschreibung.data,
            'titel': form.titel.data,
            'kategorie': form.kategorie.data,
            'anzahlTaschen': form.anzahlTaschen.data,
            'preis': form.preis.data,
            'abholStartZeit': form.abholStartZeit.data.strftime('%Y-%m-%dT%H:%M'),
            'abholEndZeit': form.abholEndZeit.data.strftime('%Y-%m-%dT%H:%M'),
            'täglicheAnzahlTaschen': form.täglicheAnzahlTaschen.data,
            'agb': form.agb.data
        }

        ref.update(updated_offer_data)
        flash('Offer successfully updated!', 'success')
        return redirect(url_for('home'))

    return render_template('offer_form.html', form=form)

@app.route('/rate_product', methods=['GET', 'POST'])
def rate_product():
    form = BewertungsFormular()
    if form.validate_on_submit():
        flash('Rating successfully submitted!', 'success')
        return redirect(url_for('index'))
    return render_template('rating_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    customer_form = AnmeldeFormular(prefix='customer')
    company_form = AnmeldeFormular(prefix='company')

    if customer_form.validate_on_submit() and customer_form.absenden.data:
        ref = db.reference('customers')
        users = ref.order_by_child('email').equal_to(customer_form.email.data).get()
        user = None
        for key, value in users.items():
            user = value
            user['id'] = key
        
        if user and check_password_hash(user['password'], customer_form.passwort.data):
            session['user_id'] = user['id']
            session['user_name'] = user.get('customername', "Unknown User")
            session['is_company'] = False
            flash('Customer logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    if company_form.validate_on_submit() and company_form.absenden.data:
        ref = db.reference('companies')
        users = ref.order_by_child('email').equal_to(company_form.email.data).get()
        user = None
        for key, value in users.items():
            user = value
            user['id'] = key
        
        if user and check_password_hash(user['password'], company_form.passwort.data):
            session['user_id'] = user['id']
            session['user_name'] = user.get('companyname', "Unknown User")
            session['is_company'] = True
            flash('Company logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login_form.html', customer_form=customer_form, company_form=company_form)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Du hast dich erfolgreich abgemeldet.', 'success')
    return redirect(url_for('login'))

@app.route('/payment', methods=['POST'])
def payment():
    try:
        anzahl = int(request.form['anzahl'])
        preis_pro_tasche = float(request.form['preis'])
        total_preis = anzahl * preis_pro_tasche
        offer_id = request.form['offer_id']

        # Speichern der Parameter in der Sitzung
        session['offer_id'] = offer_id
        session['anzahl'] = anzahl

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": url_for('payment_execute', _external=True),
                "cancel_url": url_for('payment_cancel', _external=True)},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Tasche",
                        "sku": "12345",
                        "price": str(preis_pro_tasche),
                        "currency": "EUR",
                        "quantity": anzahl}]},
                "amount": {
                    "total": str(total_preis),
                    "currency": "EUR"},
                "description": "Kauf von Taschen"}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            return "Error while creating payment"
    except Exception as e:
        return f"Error in payment route: {str(e)}"

@app.route('/payment/execute', methods=['GET'])
def payment_execute():
    try:
        payment_id = request.args.get('paymentId')
        payer_id = request.args.get('PayerID')
        anzahl = session.get('anzahl')

        if not payment_id or not payer_id or not anzahl:
            return "Fehlende Parameter", 400

        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            order_data = {
                'user_id': session['user_id'], 
                'payer_id': payer_id,
                'payment_id': payment_id,
                'preis': float(payment.transactions[0].amount.total),
                'anzahl': anzahl,
                'datum': datetime.utcnow().isoformat(),
                #Company ID MUSS NOCH ZWINGEND ERGÄNZT WERDEN
            }

            ref = db.reference('orders')
            ref.push(order_data)

            return redirect(url_for('orders'))
        else:
            return "Zahlungsabwicklung fehlgeschlagen!"
    except Exception as e:
        return f"Error in payment_execute route: {str(e)}"

@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    return "Zahlungsabwicklung abgebrochen!"

@app.route('/orders')
def orders():
    user_id = session.get('user_id')
    
    if user_id:
        ref = db.reference('orders')
        orders = ref.order_by_child('user_id').equal_to(user_id).get() 

        if not orders:
            orders = {}

        return render_template('orders.html', orders=orders)
    else:
        return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)
