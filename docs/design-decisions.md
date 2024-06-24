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

## 01: [CSS Style] 

### Meta 

Status 

: **Work in progress**  

Updated 

: 20.06.2024 

### Problem statement 

For the web application, we need a CSS file or at least some CSS to style the web application. The problem is that writing custom CSS code for the entire site is very time-consuming, and since we don't have much time, we need to find a quick solution that allows us to style the website according to our preferences. 

### Decision 

We (Majd) have decided to use Bootstrap as a framework to create the CSS styles for the website for the following reasons. Firstly, using Bootstrap offers a significantly faster development process compared to writing our own CSS file, which is crucial for us as we don't have a lot of time and want to focus on the database and the functionality of the web application. Secondly, Bootstrap includes a built-in responsive grid system that makes it easier to adapt to different screen sizes. 

### Regarded options 

|  | Pro | Contra |
| --- | --- | --- |
| **Custom CSS File** | ✔️ Full control over the styling <br> ✔️ Unique, custom design | ❌ Time-consuming |
| **Bootstrap** | ✔️ Fast development <br> ✔️ Low effort <br> ✔️ Suitable for CSS beginners | ❌ High load time due to the many Bootstrap libraries <br> ❌ Less design flexibility |

---

## [Example, delete this section] 01: How to access the database - SQL or SQLAlchemy 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-Jun-2024

### Problem statement

Should we perform database CRUD (create, read, update, delete) operations by writing plain SQL or by using SQLAlchemy as object-relational mapper?

Our web application is written in Python with Flask and connects to an SQLite database. To complete the current project, this setup is sufficient.

We intend to scale up the application later on, since we see substantial business value in it.



Therefore, we will likely:
Therefore, we will likely:
Therefore, we will likely:

+ Change the database schema multiple times along the way, and
+ Switch to a more capable database system at some point.

### Decision

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

---
