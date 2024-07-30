from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bootstrap import Bootstrap5
from forms import FirmenRegistrierungsForm, AnmeldeFormular, KundenRegistrierungsForm, AngebotsFormular, BewertungsFormular, Angebotkaufen
from my_firebase_admin import db, auth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
import paypalrestsdk
import time


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
    check_orders()
    data = request.get_json()  # POST-Anfrage wird an die Route /sessionLogin gesendet
    id_token = data.get('idToken')
    name = data.get('name')
    email = data.get('email')

    try:
        time.sleep(2)  # 2 Sekunden Verzögerung hinzufügen
        
        decoded_token = auth.verify_id_token(id_token)
        firebase_uid = decoded_token['uid']

        # Überprüfen, ob der Benutzer bereits existiert
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
        print(f"Error during token verification: {e}")  # Fehlerprotokollierung
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/favourites')
def favourites():
    check_orders()
    return render_template('favourite.html', condition=condition)

@app.route('/home')
def home():
    check_orders()
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
    check_orders()
    user_id = session.get('user_id')
    user_type = session.get('is_company')  # True für Company, False für Customer

    if user_id:
        if user_type:
            ref = db.reference(f'companies/{user_id}')
            user_data = ref.get()
        else:
            ref = db.reference(f'customers/{user_id}')
            user_data = ref.get()

        if user_data:
            user_name = user_data.get('companyname' if user_type else 'customername', "Gast")
        else:
            user_name = "Gast"
    else:
        user_name = "Gast"

    return render_template('profil.html', user_name=user_name, user_id=user_id, user_type=user_type)


@app.route('/browse')
def browse():
    check_orders()
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
    check_orders()
    ref = db.reference('offers')  # Annahme: 'offers' ist der Pfad in der Firebase-Datenbank
    offers = ref.get()  # Holen der Angebote

    if key in offers:
        offer = offers[key]
        return render_template('angebot_details.html', offer=offer, key=key)
    else:
        return "Angebot nicht gefunden", 404
    
@app.route('/Jetztkaufen/<key>')
def checkregistration(key):
    check_orders()
    user_id = session.get('user_id')
    if user_id:
        return redirect(url_for('payment', offer_id=key))
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
                'password': generate_password_hash(customer_form.passwort.data)
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
    check_orders()
    if session.get('is_company'):
        form = AngebotsFormular()
        if form.validate_on_submit():
            unternehmensID = session.get('user_id')
            kategorie = form.kategorie.data

            # Überprüfen, ob das Unternehmen bereits ein Angebot in dieser Kategorie hat
            ref = db.reference('offers')
            existing_offers = ref.order_by_child('unternehmensID').equal_to(unternehmensID).get()
            
            for key, offer in existing_offers.items():
                if offer['kategorie'] == kategorie:
                    flash('Es darf nur ein Angebot pro Kategorie erstellt werden.', 'danger')
                    return redirect(url_for('create_offer'))

            # Wenn kein Angebot in der Kategorie existiert, Angebot erstellen
            offer_data = {
                'unternehmensID': unternehmensID,
                'unternehmen': session.get('user_name'),
                'angebotsbeschreibung': form.angebotsbeschreibung.data,
                'titel': form.titel.data,
                'kategorie': kategorie,
                'anzahlTaschen': form.anzahlTaschen.data,
                'preis': form.preis.data,
                'abholStartZeit': form.abholStartZeit.data.strftime('%Y-%m-%dT%H:%M'),
                'abholEndZeit': form.abholEndZeit.data.strftime('%Y-%m-%dT%H:%M'),
                'täglicheAnzahlTaschen': form.täglicheAnzahlTaschen.data,
                'agb': form.agb.data
            }

            ref.push(offer_data)

            flash('Angebot erfolgreich erstellt!', 'success')
            return redirect(url_for('home'))

        return render_template('offer_form.html', form=form)
    else:
        flash('Du hast keine Berechtigungen!', 'danger')
        return redirect(url_for('home'))

@app.route('/edit_offer', methods=['GET'])
def edit_offer():
    check_orders()
    if not session.get('is_company'):
        flash('Du hast keine Berechtigungen!', 'danger')
        return redirect(url_for('home'))

    unternehmensID = session.get('user_id')
    ref = db.reference('offers')
    offers = ref.order_by_child('unternehmensID').equal_to(unternehmensID).get()

    return render_template('edit_offer.html', offers=offers)

@app.route('/edit_offer/<offer_id>', methods=['GET', 'POST'])
def edit_offer_details(offer_id):
    check_orders()
    if not session.get('is_company'):
        flash('Access denied. Only companies can edit offers.', 'danger')
        return redirect(url_for('home'))

    ref = db.reference(f'offers/{offer_id}')
    offer = ref.get()

    if not offer:
        flash('Offer not found.', 'danger')
        return redirect(url_for('edit_offer'))

    form = AngebotsFormular()

    if form.validate_on_submit():
        unternehmensID = session.get('user_id')
        kategorie = form.kategorie.data

        # Überprüfen, ob das Unternehmen bereits ein anderes Angebot in dieser Kategorie hat
        existing_offers = db.reference('offers').order_by_child('unternehmensID').equal_to(unternehmensID).get()

        for key, existing_offer in existing_offers.items():
            if existing_offer['kategorie'] == kategorie and key != offer_id:
                flash('Es darf nur ein Angebot pro Kategorie erstellt werden.', 'danger')
                return redirect(url_for('edit_offer_details', offer_id=offer_id))

        offer_data = {
            'titel': form.titel.data,
            'angebotsbeschreibung': form.angebotsbeschreibung.data,
            'kategorie': form.kategorie.data,
            'anzahlTaschen': form.anzahlTaschen.data,
            'preis': form.preis.data,
            'abholStartZeit': form.abholStartZeit.data.strftime('%Y-%m-%dT%H:%M'),
            'abholEndZeit': form.abholEndZeit.data.strftime('%Y-%m-%dT%H:%M'),
            'täglicheAnzahlTaschen': form.täglicheAnzahlTaschen.data,
            'agb': form.agb.data
        }

        ref.update(offer_data)
        flash('Offer successfully updated!', 'success')
        return redirect(url_for('edit_offer'))

    # Set form fields with current offer data
    if request.method == 'GET':
        form.titel.data = offer.get('titel', '')
        form.angebotsbeschreibung.data = offer.get('angebotsbeschreibung', '')
        form.kategorie.data = offer.get('kategorie', '')
        form.anzahlTaschen.data = offer.get('anzahlTaschen', 0)
        form.preis.data = offer.get('preis', 0)
        form.abholStartZeit.data = datetime.strptime(offer.get('abholStartZeit', '1900-01-01T00:00'), '%Y-%m-%dT%H:%M')
        form.abholEndZeit.data = datetime.strptime(offer.get('abholEndZeit', '1900-01-01T00:00'), '%Y-%m-%dT%H:%M')
        form.täglicheAnzahlTaschen.data = offer.get('täglicheAnzahlTaschen', False)
        form.agb.data = offer.get('agb', False)

    return render_template('edit_offer_details.html', form=form, offer_id=offer_id)

@app.route('/rate_product', methods=['GET', 'POST'])
def rate_product():
    check_orders()
    form = BewertungsFormular()
    if form.validate_on_submit():
        flash('Rating successfully submitted!', 'success')
        return redirect(url_for('index'))
    return render_template('rating_form.html', form=form)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    check_orders()
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
            session['is_company'] = False  # Setzen des Booleans für Customer
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
            session['is_company'] = True  # Setzen des Booleans für Company
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

@app.route('/payment/<offer_id>', methods=['POST'])
def payment(offer_id):
    check_orders()
    if not 'user_id' in session:
        return redirect(url_for('register'))

    try:
        anzahl = int(request.form['anzahl'])
        preis_pro_tasche = float(request.form['preis'])
        total_preis = anzahl * preis_pro_tasche

        # Speichern der Parameter in der Sitzung
        session['offer_id'] = offer_id
        session['anzahl'] = anzahl

        # Abrufen der CompanyID aus der Offer-Tabelle
        ref = db.reference(f'offers/{offer_id}')
        offer = ref.get()
        company_id = offer.get('unternehmensID')
        session['company_id'] = company_id

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
    check_orders()

    try:
        payment_id = request.args.get('paymentId')
        payer_id = request.args.get('PayerID')
        anzahl = session.get('anzahl')
        unternehmensID = session.get('company_id')

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
                'company_id': unternehmensID
            }

            # Speichern der Bestellung
            orders_ref = db.reference('orders')
            orders_ref.push(order_data)

            # Erstellen der Benachrichtigung
            notification_ref = db.reference('notifications')
            notification_ref.push({
                'order_id': payment_id,
                'date': datetime.utcnow().isoformat(),
                'status': 'unread',
                'company_id' : unternehmensID
            })

            # Setze die Session-Variable für Benachrichtigungen
            #session['has_notification'] = True

    
            print(session)

            return redirect(url_for('orders'))
        else:
            return "Zahlungsabwicklung fehlgeschlagen!"
    except Exception as e:
        return f"Error in payment_execute route: {str(e)}"

from datetime import datetime

@app.route('/notifications')
def notifications():
    check_orders()

    user_id = session.get('user_id')
    
    if user_id and session.get('is_company'):
        try:
            notification_ref = db.reference('notifications')
            notifications = notification_ref.order_by_child('company_id').equal_to(user_id).get()

            if notifications:
                # Gruppiere Benachrichtigungen nach Datum
                notifications_by_date = {}
                for key, notification in notifications.items():
                    date = notification['date'][:10]
                    if date not in notifications_by_date:
                        notifications_by_date[date] = []
                    notifications_by_date[date].append(notification)

                # Setze den Status der Benachrichtigungen auf 'read'
                for key, notification in notifications.items():
                    notification_ref.child(key).update({'status': 'read'})

                # Setze die Session-Variable zurück, nachdem die Benachrichtigungen gelesen wurden
                session['has_notification'] = False

                # Berechne das aktuelle Datum
                today = datetime.utcnow().strftime('%Y-%m-%d')

                # Übergabe der Benachrichtigungen nach Datum sortiert
                return render_template('notifications.html', notifications_by_date=notifications_by_date, today=today)
            else:
                # Berechne das aktuelle Datum
                today = datetime.utcnow().strftime('%Y-%m-%d')
                return render_template('notifications.html', notifications_by_date={}, today=today)
        except Exception as e:
            return f"Error in notifications route: {str(e)}"
    else:
        return redirect(url_for('home'))

@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    return "Zahlungsabwicklung abgebrochen!"

def check_orders():
    if 'user_id' in session:
        notification_ref = db.reference('notifications')
        notification = notification_ref.order_by_child('company_id').equal_to(session['user_id']).get()

        for key, value in notification.items():
            if value['status'] == "unread" : 
                session['has_notification'] = True
            else:
                session['has_notification'] = False

@app.route('/orders')
def orders():
    user_id = session.get('user_id')

    check_orders()
    
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
