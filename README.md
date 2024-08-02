# Inhalt dieses Repositorys

Dieses Repository ergänzt das [online notebook](https://davidhes.github.io/) 

# Setup der Web-Anwendung

**Step 1:** Aus Sicherheitsgründen ist es noch notwendig, dass Sie den Key hinzufügen, der die Verbindung zur Firebase-Datenbank erlaubt.
Zwei dieser Keys finden Sie in der HWR Cloud [hier](https://cloud.hwr-berlin.de/apps/files/files/11487569?dir=/Abgabe%20Web-Anwendung).
Alternativ finden Sie auch [hier](https://cloud.hwr-berlin.de/s/LQNnxRN7QSipbN7) die beiden Keys mit dem Passwort: M4SQsMzxJx
Fügen Sie bitte den Inhalt eines der beiden Keys in die Datei "serviceAccountKey.json". Diese befindet sich im Ordner "static\key\serviceAccountKey.json".

Begründung: Normalerweise hatten wir die "serviceAccountKey.json"-Datei in der ".gitignore"-Datei vermerkt, um sie nicht auf GitHub hochzuladen. Um Ihnen jedoch Arbeit zu ersparen, haben wir die inhaltslose Datei hochgeladen.

**Step 2:** Richten Sie eine [Python Virtual Umgebung](https://hwrberlin.github.io/fswd/python-vscode.html#32-use-the-python-virtual-environment-as-default-for-this-workspace) ein.

**Step 3:** Installieren Sie sich bitte alle Python-Pakete mittels dem Befehl "pip install -r requirements.txt" im Terminal.

```console
(venv) C:\Users\me\projects\webapp> pip install -r requirements.txt
```

**Step 4:** Nach der Installation aller notwendigen Pakete, können Sie die Anwendung mit "flask run" starten.

```console
(venv) C:\Users\me\projects\webapp> flask run
```

**Step 5:** Besuche [http://127.0.0.1:5000/home](http://127.0.0.1:5000/home) um zur Startseite zu gelangen.


# Anmeldung / Registration

**Step 1:** Sie haben die Möglichkeit, sich ein eigenes Kundenkonto bzw. Unternehmenskonto zu erstellen. Zudem können Sie sich auch optional als Kunde mit Ihrem Google-Konto anmelden.

**Step 2:** Alternativ können Sie sich aber auch mit folgenden Unternehmenskonten anmelden:

```markdown
E-Mail: baecker@mueller.de
Passwort: neuesPw!
```

```markdown
E-Mail: backshop@berlin.de
Passwort: starkesPw
```

```markdown
E-Mail: backmeister@potsdam.com
Passwort: superPw!
```

```markdown
E-Mail: kiez@baeckerei.de
Passwort: gutesPw!
```

```markdown
E-Mail: cafe@baeckerei.de
Passwort: megaPw!!
```

```markdown
E-Mail: vegan@backery.com
Passwort: neustesPw!
```

```markdown
E-Mail: konditorei@ella.de
Passwort: starkesPw!
```

Um sich mit einem Kundenkonto anzumelden, können Sie dieses nutzen:

```markdown
E-Mail: max@mustermann.de
Passwort: starkesPasswort
```

**Step 3:** Um ein Angebot kaufen zu können, haben wir die PayPal-API integriert und nutzen dabei die Sandbox-Version. 
Dafür stehen Ihnen zwei Demo-Konten zur Verfügung, die Sie für die Bezahlung verwenden können:

```markdown
E-Mail: petersilie@personal.example.com
Passwort: 1;El$p>G
```

```markdown
E-Mail: alexplatz@personal.example.com
Passwort: ;-Ju/u0Z
```

# Eventuelle Fehlerbearbeitung - Service Account Key

**Option 1:** Falls die Verbindung zur Firebase-Datenbank nicht aufgebaut werden kann, könnte dies an der "serviceAccountKey.json"-Datei liegen.
Hierfür haben wir Ihnen mehrere solcher Keys zur Verfügung gestellt, die sie alternativ nutzen können, um den aktuellen Key damit zu ersetzen. 

**Option 2:** Falls dies auch zu keiner Problemlösung führt, können Sie versuchen den Key in den Überordner zu schieben. Hier hatten wir die gesamte Projektzeit über den Key abgelegt.

**Option 3:** Kontaktieren Sie uns sehr gerne per Mail oder telefonisch, falls keiner der beiden Optionen zu einer Lösung führt.