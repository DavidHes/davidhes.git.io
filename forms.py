from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField,EmailField,SelectMultipleField, SubmitField, HiddenField, BooleanField, SelectField, DateTimeField, RadioField, IntegerField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, NumberRange, Optional
from wtforms import SelectMultipleField, widgets

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
    öffnungstage = SelectMultipleField(
        'Öffnungstage',
        choices=[('Montag', 'Montag'), ('Dienstag', 'Dienstag'), ('Mittwoch', 'Mittwoch'), 
                 ('Donnerstag', 'Donnerstag'), ('Freitag', 'Freitag'), 
                 ('Samstag', 'Samstag'), ('Sonntag', 'Sonntag')],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        default=[]
    )
    agb = BooleanField('AGB akzeptieren', validators=[InputRequired()])
    absenden = SubmitField('Erstellen')

class AnmeldeFormular(FlaskForm):
    email = EmailField('E-Mail', validators=[InputRequired(), Email()])
    passwort = PasswordField('Passwort', validators=[InputRequired(), Length(min=8)])
    absenden = SubmitField('Anmelden')

class Angebotkaufen(FlaskForm):
    JetztKaufen = SubmitField('Jetzt Kaufen!')

class Needforregistration(FlaskForm):
    BäckereiRegistierung = SubmitField('Bäckerei Registierung')
    Kundenregistierung = SubmitField('Kundenregistierung')

class KundenRegistrierungsForm(FlaskForm):
    kundenname = StringField('Nachname', validators=[InputRequired(), Length(min=5)])
    kundenVorname = StringField('Vorname', validators=[InputRequired(), Length(min=5)])
    passwort = PasswordField('Passwort', validators=[InputRequired(), Length(min=5)])
    email = EmailField('E-Mail', validators=[InputRequired(), Email()])
    absenden = SubmitField('Konto erstellen')

class AngebotsFormular(FlaskForm):
    angebotsbeschreibung = StringField('Angebotsbeschreibung', validators=[InputRequired(), Length(min=5)])
    titel = StringField('Titel', validators=[InputRequired(), Length(min=5)])
    kategorie = SelectField('Kategorie', choices=[('Brot&Brötchen', 'Brot & Brötchen'), ('Gebäck', 'Gebäck'), ('Süß', 'Süß')])
    anzahlTaschen = IntegerField('Anzahl der Taschen', validators=[InputRequired(), NumberRange(min=1)])
    preis = IntegerField('Preis', validators=[InputRequired(), NumberRange(min=1)])
    abholStartZeit = DateTimeLocalField('Abholbeginn', validators=[InputRequired()], format='%H:%M')
    abholEndZeit = DateTimeLocalField('Abholende', validators=[InputRequired()], format='%H:%M')
    täglicheAnzahlTaschen = BooleanField('Standart tägliche Anzahl von Taschen', validators=[InputRequired()])
    agb = BooleanField('AGB akzeptieren', validators=[InputRequired()])
    absenden = SubmitField('Angebot erstellen')

class FiltersFormular(FlaskForm):
    preis = IntegerField('Max Preis', validators=[Optional(), NumberRange(min=0)])
    kategorie = SelectField('Kategorie', choices=[
        ('Alle Kategorien', 'Alle Kategorien'),
        ('Brot & Brötchen', 'Brot & Brötchen'),
        ('Gebäck', 'Gebäck'),
        ('Süß', 'Süß')
    ])
    submit = SubmitField('Filtern')
    suche = StringField('Suche', validators=[Optional()])
    reset = SubmitField('Filter zurücksetzen')    

class Angebotkaufen(FlaskForm):
    JetztKaufen = SubmitField('Jetzt Kaufen!')

class BewertungsFormular(FlaskForm):
    bewertung = RadioField('Bewertung', choices=[(1, '1 Stern'), (2, '2 Sterne'), (3, '3 Sterne'), (4, '4 Sterne'), (5, '5 Sterne')], coerce=int, validators=[InputRequired()])
    rezension = StringField('Rezension', validators=[Optional()])
    absenden = SubmitField('Bewertung abgeben')

class FavoriteForm(FlaskForm):
    csrf_token = HiddenField()
