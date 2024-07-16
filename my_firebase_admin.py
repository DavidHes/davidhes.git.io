from firebase_admin import credentials, initialize_app, db

cred = credentials.Certificate('serviceAccountKey.json')
initialize_app(cred, {
    'databaseURL': 'https://plate-saver-default-rtdb.europe-west1.firebasedatabase.app'
})

# Datenbankreferenz
ref = db.reference()
