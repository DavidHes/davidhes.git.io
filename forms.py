from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, HiddenField, BooleanField, SelectField, DateTimeField, RadioField, IntegerField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, NumberRange

class FirmenRegistrierungsForm(FlaskForm):
    firmenname = StringField('Firmenname', validators=[InputRequired(), Length(min=5)])
    strasse = StringField('Straße', validators=[InputRequired(), Length(min=5)])
    hausnummer = StringField('Hausnummer', validators=[InputRequired(), Length(min=1)])
    stadt = StringField('Stadt', validators=[InputRequired(), Length(min=5)])
    postleitzahl = StringField('Postleitzahl', validators=[InputRequired(), Length(min=5)])
    passwort = PasswordField('Passwort', validators=[InputRequired(), Length(min=8)])
    email = EmailField('E-Mail', validators=[InputRequired(), Email()])
    öffnungszeit = DateTimeLocalField('Öffnungszeit', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    schließzeit = DateTimeLocalField('Schließzeit', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    agb = BooleanField('AGB akzeptieren', validators=[InputRequired()])
    absenden = SubmitField('Erstellen')

class AnmeldeFormular(FlaskForm):
    email = EmailField('E-Mail', validators=[InputRequired(), Email()])
    passwort = PasswordField('Passwort', validators=[InputRequired(), Length(min=8)])
    absenden = SubmitField('Anmelden')

class KundenRegistrierungsForm(FlaskForm):
    kundenname = StringField('Nachname', validators=[InputRequired(), Length(min=5)])
    kundenVorname = StringField('Vorname', validators=[InputRequired(), Length(min=5)])
    passwort = PasswordField('Passwort', validators=[InputRequired(), Length(min=5)])
    email = EmailField('E-Mail', validators=[InputRequired(), Email()])
    absenden = SubmitField('Konto erstellen')

class AngebotsFormular(FlaskForm):
    angebotsbeschreibung = StringField('Angebotsbeschreibung', validators=[InputRequired(), Length(min=5)])
    titel = StringField('Titel', validators=[InputRequired(), Length(min=5)])
    kategorie = SelectField('Kategorie', choices=[('tech', 'Technologie'), ('finance', 'Finanzen'), ('health', 'Gesundheitswesen')])
    anzahlTaschen = IntegerField('Anzahl der Taschen', validators=[InputRequired(), NumberRange(min=1)])
    preis = IntegerField('Preis', validators=[InputRequired(), NumberRange(min=1)])
    abholStartZeit = DateTimeLocalField('Abholbeginn', validators=[InputRequired()], format='%H:%M')
    abholEndZeit = DateTimeLocalField('Abholende', validators=[InputRequired()], format='%H:%M')
    täglicheAnzahlTaschen = BooleanField('Standart tägliche Anzahl von Taschen', validators=[InputRequired()])
    agb = BooleanField('AGB akzeptieren', validators=[InputRequired()])
    absenden = SubmitField('Angebot erstellen')

class Angebotkaufen(FlaskForm):
    JetztKaufen = SubmitField('Jetzt Kaufen!')

class BewertungsFormular(FlaskForm):
    bewertung = RadioField('Bewertung', choices=[(1, '1 Stern'), (2, '2 Sterne'), (3, '3 Sterne'), (4, '4 Sterne'), (5, '5 Sterne')], coerce=int, validators=[InputRequired()])
    rezension = StringField('Rezension', validators=[Length(min=5)])
    absenden = SubmitField('Bewertung abgeben')