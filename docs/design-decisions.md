---
title: Design Decisions
nav_order: 3
---

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

Natürlich, hier ist die Übersetzung im Markdown-Format:

## 01: [CSS Stil]

### Meta

Status: **Entschieden**

Aktualisiert: 03-Jul-2024

### Problemstellung

Für die Webanwendung benötigen wir CSS, HTML und wahrscheinlich JavaScript, um die Webanwendung zu gestalten. Das Problem ist, dass das Schreiben von individuellem CSS und JavaScript-Code für die gesamte Seite sehr zeitaufwändig ist, und da wir nicht viel Zeit haben, müssen wir eine schnelle Lösung finden, die es uns ermöglicht, die Website nach unseren Vorlieben zu gestalten.

### Entscheidung

Wir (Majd) haben beschlossen, Bootstrap als Framework zu verwenden, um das Benutzeroberflächendesign der Website aus den folgenden Gründen zu erstellen. Erstens bietet die Verwendung von Bootstrap einen deutlich schnelleren Entwicklungsprozess im Vergleich zum Schreiben eigener Dateien, was für uns entscheidend ist, da wir nicht viel Zeit haben und uns auf die Datenbank und die Funktionalität der Webanwendung konzentrieren möchten. Zweitens beinhaltet Bootstrap ein integriertes responsives Gittersystem, das die Anpassung an verschiedene Bildschirmgrößen erleichtert. Zusätzlich haben wir minimal dazu einige CSS Styles erstellt, um im Design einige Akzente zu haben und die Farbe der Webseite anzupassen.

### Betrachtete Optionen

|  | Pro | Contra |
| --- | --- | --- |
| **Eigenes CSS** | ✔️ Volle Kontrolle über das Styling <br> ✔️ Einzigartiges, individuelles Design | ❌ Zeitaufwändig |
| **Bootstrap** | ✔️ Schnelle Entwicklung <br> ✔️ Wenig Aufwand <br> ✔️ Geeignet für CSS-Anfänger | ❌ Hohe Ladezeit aufgrund der vielen Bootstrap-Bibliotheken <br> ❌ Weniger Designflexibilität |

---

## 02: [Datenbank]

### Meta

Status: **Entschieden**

Aktualisiert: 03-Jul-2024

### Problemstellung

Unser Ziel ist es, eine Datenbank für unsere Webanwendung einzurichten, in der wir unsere Daten verwalten können. Wir möchten in der Lage sein, Werte einfach hochzuladen, zu ändern und zu löschen, ohne umfangreichen Code schreiben zu müssen. Zusätzlich benötigen wir die Möglichkeit, Bilder für die Angebote der Bäckerei hochzuladen.

### Entscheidung

Unsere Entscheidung ist, Google Firebase zu verwenden. Wir haben diese Plattform gewählt, weil sie schnell und einfach zu verwenden ist, dank ihrer gut definierten Methoden. Dies vereinfacht unseren Programmierprozess, da keine langen SQL-Abfragen erforderlich sind, die oft zu kleinen, schwer erkennbaren Fehlern führen können. Außerdem haben wir bereits Erfahrung mit der Firebase Realtime Database und Storage zum Hochladen von Bildern, was für unser Projekt von Vorteil sein wird.

### Betrachtete Optionen

|  | Pro | Contra |
| --- | --- | --- |
| **Google Firebase** | ✔️ Wir wissen, wie man damit arbeitet <br> ✔️ Schnell und einfach zu verwenden, aufgrund gut definierter Methoden | ❌ SQLAlchemy nicht möglich |
| **Einfaches SQL** | ✔️ Wir wissen, wie man damit arbeitet | ❌ Bedarf an langen SQL-Abfragen |
| **SQLAlchemy** | ✔️ Keine Notwendigkeit für lange SQL-Abfragen | ❌ Wir müssen das ORM-Konzept und SQLAlchemy lernen |

---

## 03: [Zusammenarbeit]

### Meta

Status: **Entschieden**

Aktualisiert: 03-Jul-2024

### Problemstellung

Unser Ziel ist es, gleichzeitig am selben Projekt arbeiten zu können. Daher benötigen wir eine Plattform oder Werkzeuge, die die Zusammenarbeit im Team ermöglichen. Dies ist wichtig, um unorganisiertes Projektmanagement, Codekonflikte und mehr zu vermeiden.

### Entscheidung

Unsere Entscheidung ist, GitHub zu verwenden. GitHub ermöglicht es uns, gleichzeitig am selben Projekt zu arbeiten. Mit Funktionen wie Pull Requests, Code Reviews und mehr hilft uns GitHub, Änderungen zu diskutieren, Verbesserungen zu verwalten und Aufgaben zu organisieren.

Außerdem können wir mit GitHub-Repositories von überall auf den Code zugreifen und das Projekt auf jedes Gerät klonen.

### Betrachtete Optionen

Eine andere Option ist Git, aber wir bevorzugen die Verwendung von GitHub, um Repositories in die Cloud hochzuladen. So können wir Funktionen wie Pull Requests nutzen und Code Reviews direkt auf der Plattform durchführen. Auf diese Weise können wir auch Code überprüfen, Kommentare hinterlassen und die Zusammenarbeit für uns erleichtern. Außerdem haben wir viel mehr Erfahrung mit der Arbeit an Projekten auf GitHub als mit Git.

---

## 04: [Verwaltung von Formularen in der Webanwendung mit Python und Flask]

### Meta

Status: **Entschieden**

Aktualisiert: 03-Jul-2024

### Problemstellung

Wir benötigen eine Lösung, die es uns ermöglicht, einfach Formulare in unserer Webanwendung zu erstellen, zu validieren und zu verarbeiten, während wir eine sichere und hervorragende Benutzererfahrung gewährleisten. Ein entscheidender Aspekt ist die Einsparung von Entwicklungszeit, daher benötigen wir eine Lösung, die mehrere Aufgaben übernehmen kann, wie die Übertragung von Daten, deren Validierung, das Setzen von Bedingungen für die Formulare und mehr. Da die Funktionalität unserer Webanwendung stark von verschiedenen Formularen abhängt, ist die Wahl einer geeigneten Lösung entscheidend.

### Entscheidung

Wir werden Flask-WTF für die Formularverwaltung in unserer Flask-Anwendung verwenden, aus mehreren Gründen. Erstens vereinfacht Flask-WTF die Erstellung und Verwaltung von Formularen mit seiner einfach zu verwendenden Syntax und Integration mit Flask, wodurch zusätzliche Einrichtung entfällt und wir Zeit und Aufwand sparen. Darüber hinaus bietet Flask-WTF eine Vielzahl integrierter Validatoren für Benutzereingaben, die sicherstellen, dass die Eingaben korrekt und konsistent sind. Zudem ist der CSRF-Schutz standardmäßig integriert, wodurch wir Entwicklungszeit sparen und, was am wichtigsten ist, Sicherheitsrisiken reduzieren.

### Betrachtete Optionen

Wir haben drei Alternativen betrachtet:

Flask-WTF, reine WTForms oder manuell mit HTML

| Kriterium | Flask-WTF | Reine WTForms | Manuell mit HTML |
|------------------|-------------------------------------------------|----------------------------------------|-------------------------------------------|
| Benutzerfreundlichkeit | ✔️ Hoch: Integriert mit Flask. Keine Einrichtung erforderlich | ❌ Mittel: Einrichtung erforderlich | ❌ Niedrig: Manuelle Einrichtung erforderlich |
| Validierung | ✔️ Eingebaute Validatoren, CSRF-Schutz | ✔️ Validatoren sind integriert | ❌ Manuelle Validierung erforderlich |
| Sicherheit | ✔️ CSRF-Schutz standardmäßig integriert | ❌ Kein CSRF-Schutz. Einrichtung erforderlich | ❌ Manueller CSRF-Schutz erforderlich |
| Flexibilität | ✔️ Hoch: Sehr flexibel und anpassbar | ✔️ Hoch: Anpassbar | ✔️ Hoch: Volle Kontrolle |
| Lernkurve | ✔️ Niedrig: Gute Dokumentation, Flask-Integration | ❌ Mittel: Einrichtung erforderlich | ❌ Hoch: Kenntnisse von HTML und Validierungslogik erforderlich |

### 05: [Funktionen mit Flask_apscheduler verwalten] 

### Meta 

Status 

: **Entschieden**  

Aktualisiert : 28-Juli-2024 

### Problemstellung

Wir benötigen eine Lösung, die es uns ermöglicht, täglich einfach die Anzahl der Taschen in jedem Angebot in unserer Webanwendung zu aktualisieren. In diesem Fall müssen wir die Angebote, die eine Standardanzahl an Taschen haben, auf die Hauptanzahl zurücksetzen. Darüber hinaus soll dies in unserer Flask-Anwendung implementiert werden, ohne hohe Ressourcenbelastung. Daher sollte die Lösung nicht ständig laufen, sondern zu einem bestimmten Zeitpunkt und einfach zu konfigurieren und einzurichten sein, da uns Entwicklungszeit fehlt. Außerdem soll diese Funktion direkt in der Webanwendung integriert werden, um die Verwaltung zu vereinfachen.

### Entscheidung 

Wir haben uns für Cron-Trigger in Kombination mit flask_apscheduler entschieden, aus folgenden Gründen:

Präzise und komplexe Zeitpläne: Cron-Trigger ermöglichen es uns, genau festzulegen, wann die Aktualisierungen ausgeführt werden sollen, ohne dass der Code ständig im Hintergrund laufen muss.

Nahtlose Integration in unsere Flask-Webanwendung: Durch die Verwendung von flask_apscheduler können wir die Aufgaben direkt innerhalb unserer Flask-Anwendung planen und verwalten, ohne separate Cron-Dateien erstellen zu müssen.

Geringer Ressourcenverbrauch: Da der Trigger nur zu festgelegten Zeiten aktiviert wird, verbraucht er nur minimal Ressourcen und wird nicht ständig im Hintergrund ausgeführt.

Einfache Implementierung: Trotz der allgemeinen Komplexität von Cron-Syntax haben wir festgestellt, dass die Implementierung der Cron-Trigger mit flask_apscheduler sehr einfach und klar war. Wir mussten keine Cron-Dateien schreiben, sondern konnten alles in Python konfigurieren, was die Entwicklung vereinfacht hat.

### Betrachtete Optionen

Wir haben drei Alternativen betrachtet:

| Methode                        | Vorteile                                                        | Nachteile                                                |
|-------------------------------|-----------------------------------------------------------------|----------------------------------------------------------|
| flask_apscheduler             | Integration in Flask, einfache Konfiguration, Flexibilität      | Abhängigkeit von der App
 Anwendungen |
| Cron-Jobs auf dem Server      | Unabhängig von der Anwendung, stabil, systemintegriert          | Keine direkte Integration in Flask, komplexe Verwaltung, zeitaufwändig|
| Cloud-basierter Task-Scheduler| Skalierbarkeit, Verfügbarkeit, gute Integration                 | Kosten, Komplexität, Latenz, erfordert zusätzliche Infrastruktur, schwere Konfiguration |

---

### 06: [Paypal als Kaufabwicklung API] 

### Meta 

Status 

: **Entschieden**

Aktualisiert : 03-Juli-2024 

### Problemstellung

Um Bäckereien eine großartige Plattform zu bieten, auf der Funktionen wie Bestellungen, Gutscheine und Bewertungen implementiert werden können, müssen wir beim Bestellvorgang der Kunden involviert sein. Dies ermöglicht uns nicht nur die Implementierung unserer Funktionen, sondern auch zukünftige Gewinne aus den Verkäufen zu erzielen. Daher benötigen wir eine nachverfolgbare und digitale Zahlungsmethode. Angesichts unserer jungen Zielgruppe, vor allem Studenten, müssen wir diesen Aspekt in unsere Entscheidung einbeziehen.

### Entscheidung

Wir haben uns entschieden, PayPal als unsere Zahlungs-API zu verwenden, aus verschiedenen Gründen. Zum einen haben junge Nutzer selten eine Kreditkarte, daher ist die Verwendung von Kreditkarten als Zahlungsmethode für unsere Zielgruppe nicht geeignet. Da wir die Webanwendung zunächst in Deutschland starten, müssen wir eine in Deutschland beliebte Methode verwenden, weshalb wir uns für PayPal entschieden haben. Weitere Gründe sind:

Vertrauenswürdigkeit: PayPal ist eine weithin anerkannte und vertrauenswürdige Zahlungsmethode.
Einfache Integration: Es gibt umfangreiche APIs und SDKs, die die Integration in die meisten Webanwendungen erleichtern.
Sicherheit: PayPal bietet robuste Sicherheitsmaßnahmen und Betrugsschutz.

### Betrachtete Optionen

Wir haben weitere Alternativen betrachtet: Kredit-/Debitkarten, Apple Pay/Google Pay und Klarna.

| Kriterium                    | PayPal                                             | Kredit-/Debitkarten                                 | Apple Pay/Google Pay                               | Klarna                                              |
|------------------------------|----------------------------------------------------|----------------------------------------------------|---------------------------------------------------|----------------------------------------------------|
| **Benutzerfreundlichkeit**   | ✔️ Hoch: Weit verbreitet und einfach zu nutzen     | ✔️ Hoch: Sehr verbreitet und sofort nutzbar        | ✔️ Hoch: Einfache und schnelle Nutzung             | ✔️ Hoch: Bequem, besonders mit Rechnungskauf       |
| **Sicherheit**               | ✔️ Hoch: Robuste Sicherheitsmaßnahmen und Betrugsschutz | ❌ Mittel: Risiko von Datenmissbrauch               | ✔️ Hoch: Token-basierte Sicherheit                 | ✔️ Hoch: Klarna übernimmt das Zahlungsausfallrisiko |
| **Einfachheit der Integration** | ✔️ Hoch: Umfangreiche APIs und SDKs verfügbar   | ✔️ Hoch: Direkte Abwicklung, einfache Integration  | ✔️ Hoch: Unterstützung durch viele Payment-Gateways | ❌ Mittel: Komplexere Integration erforderlich       |
| **Studentenfreundlichkeit**  | ✔️ Hoch: Viele Studenten haben PayPal-Konten      | ❌ Mittel: Nicht alle Studenten haben Kreditkarten | ✔️ Hoch: Viele Studenten haben Apple/Android Geräte | ✔️ Hoch: Besonders attraktiv durch Rechnungskauf    |
