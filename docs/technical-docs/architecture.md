---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }

{: .no_toc }
# Architecture

> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

### Overview

## Frontend:

# HTML-Templates:
Definieren die Struktur und den Inhalt der Webseiten und ermöglichen die Darstellung dynamischer Daten. 

# Bootstrap:
Ein Framework für responsive und moderne Weblayouts mit vordefinierten CSS-Klassen und JavaScript-Komponenten. Es erleichtert das schnelle Erstellen ansprechender und konsistenter Benutzeroberflächen.

# Flask WTForms (Formulargenerierung und -validierung im Frontend):
Erstellung und Validierung von HTML-Formularen im Browser. Es bietet eine bequeme Möglichkeit, Formulare zu generieren und zu validieren, bevor sie an den Server gesendet werden.

# Jinja-Templates:
Ermöglichen die dynamische Generierung von HTML durch Einbettung von Python-Code. Jinja-Templates bieten eine flexible Möglichkeit, Inhalte und Layouts zu gestalten und Daten aus dem Backend an das Frontend zu übergeben.

## Backend:

# Flask (Routing und HTTP-Anfragen-Verarbeitung):
Für die Verwaltung von Routen und die Verarbeitung von HTTP-Anfragen. Es ermöglicht die Definition von Endpunkten und die Verarbeitung von eingehenden Anfragen.

# Python (Geschäftslogik):
Implementierung der Kernfunktionalität der Anwendung. Python wird verwendet, um die Logik zu schreiben, die die Anwendung antreibt.

# Flask WTForms (Formularvalidierung im Backend):
Serverseitige Validierung der Formulardaten. Stellt sicher, dass die Daten korrekt und sicher sind, bevor sie verarbeitet oder in die Datenbank gespeichert werden.

# Firebase (Datenbankinteraktionen):
Echtzeit-Datenbank und Backend-Dienste wie Authentication und Realtime database. Firebase bietet eine skalierbare Datenbanklösung und Backend-Dienste, die die Entwicklung und Verwaltung von Anwendungen vereinfachen. 

# PayPal API (Zahlungsabwicklung):
Integration von Zahlungsfunktionen in die Anwendung. Die PayPal API ermöglicht sichere und effiziente Zahlungsabwicklungen innerhalb der Anwendung.
