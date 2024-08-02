from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bootstrap import Bootstrap5
import requests
from forms import FirmenRegistrierungsForm, AnmeldeFormular,FiltersFormular, FavoriteForm, KundenRegistrierungsForm, AngebotsFormular, BewertungsFormular, Angebotkaufen
from my_firebase_admin import db, auth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
import paypalrestsdk
from flask_apscheduler import APScheduler
import pytz
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
    "mode": "sandbox",  
    "client_id": "AUJPGXC_Q2irXahFthN6EpW2PAW6E-Seh_j1AEcGpDcsbNlL8oyCWJaQ06D4-ourzL3qrOx7pifp6Zj9",
    "client_secret": "EHn6JQE0eJ-EfOflg8w1E4ogCDJrSPgcqnir2PvB_0DgpYh5L7y4G6q8Doi1fsPaXf9CJeYxO8nJw7kW"
})

@app.route('/firebase_auth_and_register', methods=['POST'])
def firebase_auth_and_register():
    check_orders()
    data = request.get_json()  
    id_token = data.get('idToken')
    name = data.get('name')
    email = data.get('email')

    try:        
        decoded_token = auth.verify_id_token(id_token)
        firebase_uid = decoded_token['uid']

        ref = db.reference('customers')
        existing_users = ref.order_by_child('email').equal_to(email).get()

        user_id = None
        if not existing_users:
            customer_data = {
                'customerFirstName': name.split()[0], 
                'customername': name,  
                'email': email,
                'firebase_uid': firebase_uid,
                'is_company': False
            }
            new_user_ref = ref.push(customer_data)
            user_id = new_user_ref.key
        else:
            for key, value in existing_users.items():
                user_id = key

        session['user_id'] = user_id  
        session['user_name'] = name
        session['is_company'] = False

        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Fehler bei der token verification: {e}")  
        return jsonify({'success': False, 'error': str(e)}), 401
    
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

    review_ids = ['-O3FIv9RwHwFmiZ3UGw6', '-O3DL0eMYlzvep1F_pHZ', '-O3FIdPWneHU1APEdpsn']

    reviews_ref = db.reference('ratings') 
    reviews = []

    for review_id in review_ids:
        review_data = reviews_ref.child(review_id).get()
        if review_data:
            review_user_id = review_data.get('user')
            if review_user_id:
                user_ref = db.reference(f'customers/{review_user_id}')
                user_data = user_ref.get()
                if user_data:
                    firstname = user_data.get('customerFirstName', '')
                    lastname = user_data.get('customerName', '')
                    full_name = f"{firstname} {lastname}"
                else:
                    full_name = 'Anonym'
            else:
                full_name = 'Anonym'
            reviews.append({
                'name': full_name,
                'review': review_data.get('rezension', '') 
            })

    return render_template('home.html', user_name=user_name, user_id=user_id, reviews=reviews, enumerate=enumerate)

@app.route('/profil')
def profil():
    check_orders()
    user_id = session.get('user_id')
    user_type = session.get('is_company')  

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

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    check_orders()
  
    form = FiltersFormular()
    offers_ref = db.reference('offers')
    companies_ref = db.reference('companies')
    ratings_ref = db.reference('ratings')

    offers = offers_ref.get() or {}
    companies = companies_ref.get() or {}
    ratings = ratings_ref.get() or {}

    max_price = None
    category = 'Alle Kategorien'
    search_term = None
    current_day = datetime.now(pytz.timezone('Europe/Berlin')).strftime('%A')

    wochentage_deutsch = {
        'Monday': 'Montag',
        'Tuesday': 'Dienstag',
        'Wednesday': 'Mittwoch',
        'Thursday': 'Donnerstag',
        'Friday': 'Freitag',
        'Saturday': 'Samstag',
        'Sunday': 'Sonntag'
    }
    
    aktueller_wochentag = wochentage_deutsch.get(current_day, 'Unbekannter Tag')
    print(aktueller_wochentag)

    if form.validate_on_submit():
        if form.reset.data:  
            return redirect(url_for('browse'))

        max_price = form.preis.data if form.preis.data else None
        category = form.kategorie.data if form.kategorie.data else 'Alle Kategorien'
        search_term = form.suche.data

    if category != 'Alle Kategorien' and max_price is not None:
        offers = {key: offer for key, offer in offers.items() if offer['kategorie'] == category and offer['preis'] <= max_price}
    elif category != 'Alle Kategorien':
        offers = {key: offer for key, offer in offers.items() if offer['kategorie'] == category}
    elif max_price is not None:
        offers = {key: offer for key, offer in offers.items() if offer['preis'] <= max_price}
    
    if search_term:
        offers = {key: offer for key, offer in offers.items() if search_term.lower() in offer['titel'].lower() or search_term.lower() in offer['angebotsbeschreibung'].lower()}    

    for offer_key, offer in offers.items():
        company_id = offer['unternehmensID']
        company = companies.get(company_id, {})

        print("Infos der Unternehmen")
        print(company)
        print(current_day)

        if aktueller_wochentag not in company.get('öffnungstage', []):
            print(company.get('öffnungstage', []))
            offers[offer_key]['is_available'] = False
        elif offer['anzahlTaschenToday'] <= 0:
            offers[offer_key]['is_available'] = False
        else:
            offers[offer_key]['is_available'] = True

        company_ref = db.reference(f'companies/{company_id}')
        company_data = company_ref.get()
        if company_data:
            strasse = company_data.get('street', '')
            nummer = company_data.get('number', '')
            plz = company_data.get('postcode', '')
            stadt = company_data.get('city', '') 
            adresse = f"{strasse} {nummer}, {plz} {stadt}"
            offers[offer_key]['adresse'] = adresse 

    page = request.args.get('page', 1, type=int)
    per_page = 9
    total = len(offers)
    start = (page - 1) * per_page
    end = start + per_page

    total_pages = (total + per_page - 1) // per_page
    print(ratings)

    offer_ratings = {}

    for offer_id, offer in offers.items():
        total_rating = 0
        rating_count = 0
        for rating in ratings.values():
            if rating['offerid'] == offer_id:
                total_rating += rating['bewertung']
                rating_count += 1
        if rating_count > 0:
            average_rating = round(total_rating / rating_count, 1)
        else:
            average_rating = 0

        offer_ratings[offer_id] = {
            'average_rating': average_rating,
            'total_rating': total_rating,
            'rating_count': rating_count,
            'offerid': offer_id
        }

    offers = dict(list(offers.items())[start:end])
    
    total_pages = max(total_pages, 1)
    
    return render_template('browse.html', offers=offers, offer_ratings=offer_ratings, page=page, total_pages=total_pages, form=form)

@app.route('/add_to_favourites/<key>', methods=['POST'])
def add_to_favourites(key):
    check_orders()

    user_id = session.get('user_id')

    if user_id:
        ref = db.reference('favourites')
        existing_favourites = ref.order_by_child('user').equal_to(user_id).get()

        for fav_key, fav in existing_favourites.items():
            if fav['offerid'] == key:
                flash("Du hast dieses Angebot bereits favorisiert.", "warning")
                return redirect(url_for('browse'))

        fav_data = {
            'user': user_id,
            'offerid': key,
        }
        ref.push(fav_data)
        flash("Angebot wurde zu deinen Favoriten hinzugefügt.", "success")
        return redirect(url_for('browse'))
    else:
        flash("Du musst dich anmelden, um Favoriten hinzuzufügen.", "danger")
        return redirect(url_for('register'))

     
@app.route('/favourites')
def favourites():
    check_orders()

    user_id = session.get('user_id') 

    if not user_id:
        flash("Du musst dich anmelden, um deine Favoriten sehen zu können!", "danger")
        return redirect(url_for('login'))  

    refoffers = db.reference('offers')  
    offers = refoffers.get() or {}    

    ref = db.reference('favourites')  
    favs = ref.order_by_child('user').equal_to(user_id).get() 

    if not favs:
        favs = {}

    print(f"favs: {favs}")
    print(f"Type of favs: {type(favs)}")

    company_ids = {offer['unternehmensID'] for offer in offers.values()}

    companies_ref = db.reference('companies')
    companies_data = {company_id: companies_ref.child(company_id).get() for company_id in company_ids}

    for fav_key, fav in favs.items():
        offer_id = fav['offerid']
        if offer_id in offers:
            offer = offers[offer_id]
            company_id = offer['unternehmensID']
            if company_id in companies_data:
                company = companies_data[company_id]
                strasse = company.get('street', '')
                nummer = company.get('number', '')
                plz = company.get('postcode', '')
                stadt = company.get('city', '') 
                adresse = f"{strasse} {nummer}, {plz} {stadt}"
                offer['adresse'] = adresse

    form = FavoriteForm()

    return render_template('favourite.html', favs=favs, offers=offers, form=form) 


@app.route('/update_favourite/<favid>', methods=['POST'])
def update_favourite(favid):
    check_orders()

    user_id = session.get('user_id')
    offer_id = favid

    if not user_id:
        return redirect(url_for('register'))  

    ref = db.reference('favourites')
    favs = ref.order_by_child('user').equal_to(user_id).get()
    
    for key, fav in favs.items():
        if fav['offerid'] == offer_id:
         already_favourited = True

    if already_favourited:
            for key, fav in favs.items():
                if fav['offerid'] == favid:
                    ref.child(key).delete()
                    break
    else:
            ref.push({
                'user': user_id,
                'offerid': offer_id
            })

    return redirect(url_for('favourites'))

@app.route('/angebot/<key>')
def angebot_details(key):
    check_orders()
    ref = db.reference('offers')  
    offers = ref.get()  

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
            ref = db.reference('customers')
            existing_users = ref.order_by_child('email').equal_to(customer_form.email.data).get()

            if existing_users:
                flash('Diese E-Mail existiert bereits! Bitte logge dich ein!', 'danger')
                return redirect(url_for('login'))

            customer_data = {
                'customerFirstName': customer_form.kundenVorname.data,
                'customername': customer_form.kundenname.data,
                'email': customer_form.email.data,
                'password': generate_password_hash(customer_form.passwort.data)
            }

            ref.push(customer_data)
            flash('Kunden-Registrierung erfolgreich!', 'success')
            return redirect(url_for('login'))

        elif company_form.validate_on_submit():
            ref = db.reference('companies')
            existing_users = ref.order_by_child('email').equal_to(company_form.email.data).get()

            if existing_users:
                flash('Diese E-Mail existiert bereits! Bitte logge dich ein!', 'danger')
                return redirect(url_for('login'))

            company_data = {
                'companyname': company_form.firmenname.data,
                'street': company_form.strasse.data,
                'number': company_form.hausnummer.data,
                'city': company_form.stadt.data,
                'postcode': company_form.postleitzahl.data,
                'password': generate_password_hash(company_form.passwort.data),
                'email': company_form.email.data,
                'öffnungstage': company_form.öffnungstage.data,
                'terms': company_form.agb.data
            }

            ref.push(company_data)
            flash('Unternehmens-Registrierung erfolreich!', 'success')
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

            ref = db.reference('offers')
            existing_offers = ref.order_by_child('unternehmensID').equal_to(unternehmensID).get()
            
            for key, offer in existing_offers.items():
                if offer['kategorie'] == kategorie:
                    flash('Es darf nur ein Angebot pro Kategorie erstellt werden!', 'danger')
                    return redirect(url_for('create_offer'))
                
            offer_data = {
                'unternehmensID': unternehmensID,
                'unternehmen': session.get('user_name'),
                'angebotsbeschreibung': form.angebotsbeschreibung.data,
                'titel': form.titel.data,
                'kategorie': kategorie,
                'anzahlTaschen': form.anzahlTaschen.data,
                'anzahlTaschenToday': form.anzahlTaschen.data,
                'standartanzahlTaschen': form.anzahlTaschen.data,
                'preis': form.preis.data,
                'altPreis': form.altPreis.data,
                'abholStartZeit': form.abholStartZeit.data.strftime('%H:%M'),
                'abholEndZeit': form.abholEndZeit.data.strftime('%H:%M'),
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
        flash('Du hast keine Berechtigungen!', 'danger')
        return redirect(url_for('home'))

    ref = db.reference(f'offers/{offer_id}')
    offer = ref.get()

    if not offer:
        flash('Dieses Angebot wurde nicht gefunden!', 'danger')
        return redirect(url_for('edit_offer'))

    form = AngebotsFormular()

    if form.validate_on_submit():
        unternehmensID = session.get('user_id')
        kategorie = form.kategorie.data

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
            'StandartanzahlTaschen': form.anzahlTaschen.data,
            'preis': form.preis.data,
            'altPreis': form.altPreis.data,
            'abholStartZeit': form.abholStartZeit.data.strftime('%H:%M'),
            'abholEndZeit': form.abholEndZeit.data.strftime('%H:%M'),
            'täglicheAnzahlTaschen': form.täglicheAnzahlTaschen.data,
            'agb': form.agb.data
        }

        ref.update(offer_data)
        flash('Offer successfully updated!', 'success')
        return redirect(url_for('edit_offer'))

    if request.method == 'GET':
        form.titel.data = offer.get('titel', '')
        form.angebotsbeschreibung.data = offer.get('angebotsbeschreibung', '')
        form.kategorie.data = offer.get('kategorie', '')
        form.anzahlTaschen.data = offer.get('anzahlTaschen', 0)
        form.preis.data = offer.get('preis', 0)
        form.altPreis.data = offer.get('altPreis', 0)
        form.abholStartZeit.data = datetime.strptime(offer.get('abholStartZeit', '00:00'), '%H:%M').time()
        form.abholEndZeit.data = datetime.strptime(offer.get('abholEndZeit', '00:00'), '%H:%M').time()
        form.täglicheAnzahlTaschen.data = offer.get('täglicheAnzahlTaschen', False)
        form.agb.data = offer.get('agb', False)

    return render_template('edit_offer_details.html', form=form, offer_id=offer_id)

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
            session['is_company'] = False  
            flash('Erfolgreich angemeldet.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Die E-Mail oder das Passwort ist falsch!', 'danger')

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
            flash('Erfolgreich angemeldet.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Die E-Mail oder das Passwort ist falsch!', 'danger')
    
    return render_template('login_form.html', customer_form=customer_form, company_form=company_form)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Du hast dich erfolgreich abgemeldet.', 'success')
    return redirect(url_for('login'))

@app.route('/payment/<key>', methods=['POST'])
def payment(key):
    check_orders()
    if not 'user_id' in session:
        return redirect(url_for('register'))

    try:
        anzahl = int(request.form['anzahl'])
        preis_pro_tasche = float(request.form['preis'])
        total_preis = anzahl * preis_pro_tasche

        session['anzahl'] = anzahl

        ref = db.reference(f'offers/{key}')
        offer = ref.get()
        company_id = offer.get('unternehmensID')
        session['company_id'] = company_id

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": url_for('payment_execute', _external=True, key=key),
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
            return "Fehler bei der Paymentgenerierung"
    except Exception as e:
        return f"Fehler: {str(e)}"


@app.route('/payment/execute/<key>', methods=['GET'])
def payment_execute(key):
    try:
        payment_id = request.args.get('paymentId')
        payer_id = request.args.get('PayerID')
        anzahl = session.get('anzahl')
        unternehmensID = session.get('company_id')
        user_id = session['user_id']

        if not payment_id or not payer_id or not anzahl:
            return "Fehlende Parameter", 400
        
        customer_ref = db.reference(f'customers/{user_id}')
        customer_data = customer_ref.get()
        if customer_data:
            firstname = customer_data.get('customerFirstName', '')
            lastname = customer_data.get('customerName', '')
            full_name = f"{firstname} {lastname}"
        else:
            full_name = "Unternehmensbestellung"

        company_ref = db.reference(f'companies/{unternehmensID}')
        company_data = company_ref.get()
        if company_data:
            unternehmen = company_data.get('companyname', '')
            strasse = company_data.get('street', '')
            nummer = company_data.get('number', '')
            plz = company_data.get('postcode', '')
            stadt = company_data.get('city', '') 
            adresse = f"{strasse} {nummer}, {plz} {stadt}"
        else:
            unternehmen = "Unternehmensbestellung"    

        order_ref = db.reference(f'offers/{key}')
        order_data = order_ref.get()
        if order_data:
            beginn = order_data.get('abholStartZeit', '')
            ende = order_data.get('abholEndZeit', '')
            abholzeitraum = f"{beginn} - {ende}"
            kategorie = order_data.get('kategorie')

        else:
            abholzeitraum = "Undefiniert"

        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            order_data = {
                'user_id': user_id,
                'full_name': full_name,
                'payer_id': payer_id,
                'payment_id': payment_id,
                'preis': float(payment.transactions[0].amount.total),
                'anzahl': anzahl,
                'datum': datetime.utcnow().isoformat(),
                'offer_id': key,
                'status': "ausstehend",
                'company_id': unternehmensID,
                'unternehmen': unternehmen,
                'adresse': adresse,
                'abholzeitraum': abholzeitraum
            }

            orders_ref = db.reference('orders')
            new_order_ref = orders_ref.push(order_data)
            order_id = new_order_ref.key  

            offer_ref = db.reference(f'offers/{key}')
            offer_data = offer_ref.get()
            if offer_data:
                aktuelle_anzahl = offer_data.get('anzahlTaschenToday', 0)
                neue_anzahl = aktuelle_anzahl - int(anzahl)
                offer_ref.update({'anzahlTaschenToday': neue_anzahl})

            notification_ref = db.reference('notifications')
            notification_ref.push({
                'payment_id': payment_id,
                'user_id': user_id,
                'full_name': full_name,
                'preis': float(payment.transactions[0].amount.total),
                'anzahl': anzahl,
                'date': datetime.utcnow().isoformat(),
                'status': 'unread',
                'company_id': unternehmensID,
                'order_id': order_id,
                'abholzeitraum': abholzeitraum,
                'kategorie': kategorie
            })

            print(session)

            return redirect(url_for('orders'))
        else:
            print("Zahlungsabwicklung fehlgeschlagen:", payment.error)
            return "Zahlungsabwicklung fehlgeschlagen!"
    except Exception as e:
        print("Fehler:", str(e))
        return f"Fehler: {str(e)}"


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
                notifications_list = list(notifications.items())

                notifications_by_date = {}
                for key, notification in notifications_list:
                    date = notification['date'][:10]
                    if date not in notifications_by_date:
                        notifications_by_date[date] = []
                    notifications_by_date[date].append(notification)

                page = request.args.get('page', 1, type=int)
                per_page = 4 
                total_days = len(notifications_by_date)
                start = (page - 1) * per_page
                end = start + per_page

                total_pages = (total_days + per_page - 1) // per_page

                paginated_notifications_by_date = dict(list(notifications_by_date.items())[start:end])

                for key, notification in notifications_list:
                    notification_ref.child(key).update({'status': 'read'})

                session['has_notification'] = False

                today = datetime.utcnow().strftime('%Y-%m-%d')

                return render_template('notifications.html', notifications_by_date=paginated_notifications_by_date, today=today, page=page, total_pages=total_pages)
            else:
                today = datetime.utcnow().strftime('%Y-%m-%d')
                return render_template('notifications.html', notifications_by_date={}, today=today, page=1, total_pages=1)
        except Exception as e:
            return f"Fehler: {str(e)}"
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

    if not user_id:
        return redirect(url_for('register'))
    
    check_orders()
    
    ref = db.reference('orders')
    orders = ref.order_by_child('user_id').equal_to(user_id).get()

    if not orders:
        orders = {}

    print("Ursprüngliche Bestellungen:", orders)

    orders = dict(sorted(orders.items(), key=lambda item: item[1]['datum'], reverse=True))

    for key, order in orders.items():
        try:
            date = datetime.strptime(order['datum'], '%Y-%m-%dT%H:%M:%S.%f')
            order['datum'] = date.strftime('%d.%m.%Y')
        except ValueError:
            order['datum'] = order['datum']  

    print("Formatierte Bestellungen:", orders)

    page = request.args.get('page', 1, type=int)  
    per_page = 9  
    total = len(orders) 
    start = (page - 1) * per_page  
    end = start + per_page 
    total_pages = (total + per_page - 1) // per_page

    orders = dict(list(orders.items())[start:end])

    print("Bestellungen für Seite", page, ":", orders)

    return render_template('orders.html', orders=orders, page=page, total_pages=total_pages)

@app.route('/order/<key>', methods=['GET', 'POST'])
def certain_order(key):
    user_id = session.get('user_id')

    if not user_id:
        flash("Du musst dich anmelden, um deine Bestellungen sehen zu können!", "danger")
        return redirect(url_for('login')) 

    ref = db.reference('orders')
    orders = ref.get()

    if key not in orders:
        flash("Order not found", "danger")
        return redirect(url_for('orders'))  

    order = orders[key]

    refrating = db.reference('ratings')
    ratings = refrating.order_by_child('orderid').equal_to(key).get()

    if ratings:
        unrated = False
    else:
        unrated = True

    if request.method == 'POST':
        if 'mark_as_completed' in request.form:
            ref.child(key).update({'status': 'abgeschlossen'})
            flash("Deine Bestellung wurde als abgeholt vermerkt.", "success")
            return redirect(url_for('certain_order', key=key, unrated=unrated))

    return render_template('certain_order.html', order=order, key=key, unrated=unrated)

@app.route('/ratenow/<key>',  methods=['GET', 'POST'])
def ratenow(key):
    form = BewertungsFormular()
    user_id = session.get('user_id')  

    if user_id:
        ref = db.reference('orders')
        orders = ref.get()
        if key in orders:
         order = orders[key]
        
    if form.validate_on_submit():
        rating_data = {
            'bewertung': form.bewertung.data,
            'rezension': form.rezension.data,
            'user': user_id,
            'orderid': key,
            'offerid': order['offer_id']
        }
        ref = db.reference('ratings')
        ref.push(rating_data)
        
        flash("Vielen Dank für deine Bewertung!", "success")
        return redirect(url_for('profil'))
    
    return render_template('rating_form.html', form=form, condition=condition)

def reset_taschen():
    offers_ref = db.reference('offers')
    offers = offers_ref.get()

    if not offers:
        return "No offers found"
    
    for key, offer in offers.items():
        if offer['täglicheAnzahlTaschen'] == False:
            offers_ref.child(key).update({'anzahlTaschenToday': 0})
        else:
            offers_ref.child(key).update({'anzahlTaschenToday': offer['anzahlTaschen']})

        print(offer['anzahlTaschen']) 

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(id='Daily Task', func=reset_taschen, trigger='cron', hour=0, minute=0)

if __name__ == "__main__":
        app.run()