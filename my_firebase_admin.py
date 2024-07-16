from firebase_admin import credentials, initialize_app, db

cred = credentials.Certificate('serviceAccountKey.json')
initialize_app(cred, {
    'databaseURL': 'https://plate-saver-default-rtdb.europe-west1.firebasedatabase.app'
})

# Datenbankreferenz
ref = db.reference()



##cred = credentials.Certificate('C:/Users/David/Documents/Studium/SoSe24/Entwicklung von Web-Anwendungen/wirklich final/davidhes.github.io/serviceAccountKey.json')
##initialize_app(cred, {
  ##  'databaseURL': 'https://plate-saver-default-rtdb.europe-west1.firebasedatabase.app'
##})

# Datenbankreferenz
#ref = db.reference()
