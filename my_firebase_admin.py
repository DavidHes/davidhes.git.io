from firebase_admin import credentials, initialize_app, db, auth

cred = credentials.Certificate('static\key\serviceAccountKey.json')
initialize_app(cred, {
    'databaseURL': 'https://plate-saver-default-rtdb.europe-west1.firebasedatabase.app'
})

# Datenbankreferenz
ref = db.reference()
