---
title: Data Model
parent: Technical Docs
nav_order: 2
---

# Firebase Realtime Database Datenmodell

Dieses Dokument beschreibt das Datenmodell der Firebase Realtime Database. Die Datenstruktur ist hierarchisch organisiert und besteht aus verschiedenen Hauptknoten. Jeder Knoten enthält spezifische Datentypen und Informationen.

# Die `companies`-Collection enthält Dokumente, die Informationen über verschiedene Unternehmen speichern.

```json
{
  "company_id": {
    "city": "string",
    "companyname": "string",
    "email": "string",
    "number": "string",
    "password": "string",
    "postcode": "string",
    "street": "string",
    "terms": "boolean",
    "öffnungstage": [
      "string"
    ]
  }
}
```

# Die customers-Collection enthält Dokumente, die Informationen über Kunden speichern.

```json
{
  "customer_id": {
    "email": "string",
    "is_company": "boolean",
    "customerFirstName": "string",
    "customername": "string",
    "password": "string",
    "firebase_uid": "string" (optional)
  }
}
```

# Die favourites-Collection speichert, welche Angebote ein Benutzer favorisiert hat.

```json
{
  "favourite_id": {
    "offerid": "string",
    "user": "string"
  }
}
```

# Die messages-Collection enthält Nachrichten, die zwischen Benutzern ausgetauscht wurden.

```json
{
  "message_id": "string"
}

# Die notifications-Collection speichert Benachrichtigungen für Benutzer und Unternehmen.

{
  "notification_id": {
    "company_id": "string",
    "date": "string" (ISO 8601 Datumsformat),
    "order_id": "string",
    "status": "string"
  }
}
```

# Die offers-Collection enthält Angebote, die von Unternehmen bereitgestellt werden.

```json
{
  "offer_id": {
    "abholEndZeit": "string",
    "abholStartZeit": "string",
    "agb": "boolean",
    "altPreis": "number",
    "angebotsbeschreibung": "string",
    "anzahlTaschen": "number",
    "kategorie": "string",
    "preis": "number",
    "standartanzahlTaschen": "number",
    "titel": "string",
    "täglicheAnzahlTaschen": "boolean",
    "unternehmen": "string",
    "unternehmensID": "string"
  }
}
```

```json
# Die orders-Collection enthält Bestellungen, die von Benutzern getätigt wurden.

{
  "order_id": {
    "anzahl": "number",
    "company_id": "string",
    "datum": "string" (ISO 8601 Datumsformat),
    "offer_id": "string",
    "payer_id": "string",
    "payment_id": "string",
    "preis": "number",
    "status": "string",
    "user_id": "string"
  }
}
```

# Die ratings-Collection speichert Bewertungen für Angebote.

```json
{
  "rating_id": {
    "bewertung": "number",
    "offerid": "string",
    "orderid": "string",
    "rezension": "string",
    "user": "string"
  }
}

# Der schlüssel-Knoten enthält allgemeine Schlüssel-Wert-Paare.

{
  "schlüssel": "string"
}
```
