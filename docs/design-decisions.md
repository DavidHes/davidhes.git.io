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

Status: **Decided**  

Updated: 03-Jul-2024 

### Problem statement 

For the web application, we need CSS, HTML and probably JavaScript to style the web application. The problem is that writing custom CSS and JavaScript code for the entire site is very time-consuming, and since we don't have much time, we need to find a quick solution that allows us to style the website according to our preferences. 

### Decision 

We (Majd) have decided to use Bootstrap as a framework to create the User Interface design of the website for the following reasons. Firstly, using Bootstrap offers a significantly faster development process compared to writing our own files, which is crucial for us as we don't have a lot of time and want to focus on the database and the functionality of the web application. Secondly, Bootstrap includes a built-in responsive grid system that makes it easier to adapt to different screen sizes. 

### Regarded options 

|  | Pro | Contra |
| --- | --- | --- |
| **Custom CSS File** | ✔️ Full control over the styling <br> ✔️ Unique, custom design | ❌ Time-consuming |
| **Bootstrap** | ✔️ Fast development <br> ✔️ Low effort <br> ✔️ Suitable for CSS beginners | ❌ High load time due to the many Bootstrap libraries <br> ❌ Less design flexibility |

---

## 02: [Database] 

### Meta 

Status: **Decided**  

Updated: 03-Juli-2024 

### Problem statement 

Our goal is to set up a database for our web application where we can manage our data. We want to be able to upload, change and delete values easily, without writing extensive code. Additionally, we need the capability to upload pictures for the bakery's offers. 

### Decision 

Our decision is to use Google Firebase. We chose this platform because it is fast and easy to use, thanks to its well-defined methods. This simplifies our programming process, eliminating the need for lengthy SQL queries that can often lead to small, hard-to-detect mistakes. Also, we already have some experience with Firebase's Realtime Database and Storage for uploading pictures, which will be beneficial for our project. 

### Regarded options 

|  | Pro | Contra |
| --- | --- | --- |
| **Google Firebase** | ✔️ We know how to write <br> ✔️ Fast and easy to use, because of well-defined methods  | ❌ SQLAlchemy not possible |
| **Plain Sql** | ✔️ We know how to write | ❌ Need for lengthy SQL queries |
| **SQLAlchemy** | ✔️ No need for lengthy SQL queries | ❌ We must learn ORM concept & SQLAlchemy |

---

## 03: [Collaboration] 

### Meta 

Status: **Decided**  

Updated: 03-Juli-2024

### Problem statement 

Our goal is to enable to work simultaneously on the same project, therefore we need a platform or tools to enable collaboration among the team. This is important to avoid Unorganized Project Management, Code Conflicts and more. 

### Decision 

Our decision is to use GitHub. GitHub allows us to work on the same project simultaneously. With Features like pull requests, code reviews, and more GitHub helps us discuss changes, improvements, and manage tasks.  

Also having GitHub repositories, we can access the code from everywhere and clone the project to every device. 

### Regarded options

Other option is Git, but we prefer using GitHub to upload repositories to the cloud and this way, we can use features like pull requests and conduct code reviews directly on the platform. This way we can also review code, leave comments, and establish easier collaboration for us. Furthermore, we're have way more experience with working on projects on GitHub than on Git. 

---

### 04: [Managing Forms in Web App with Python and Flask] 

### Meta 

Status 

: **Decided**  

Updated : 03-Juli-2024 

### Problem statement 

We need a solution that allows us to easily create, validate, and process forms in our web application while ensuring a secure and excellent user experience. A crucial aspect is saving development time, so we require a solution that can handle multiple tasks, such as transferring data, validating it, setting conditions for the forms, and more. Given that our web app's functionality heavily depends on various forms, choosing a suitable solution is essential. 

### Decision 

We will use Flask-WTF for form handling in our Flask application for several reasons. Firstly, Flask-WTF simplifies the creation and management of forms with its easy-to-use syntax and integration with Flask, eliminating the need for additional setup and saving us time and effort. Additionally, Flask-WTF provides a wide range of built-in validators for user input, ensuring that input is correct and consistent. Moreover, CSRF protection is built-in by default, allowing us to save development time and, most importantly, reduce security risks. 

### Regarded options 

We regarded three alternative options: 

Flask-WTF,Pure WTForms or Manually with HTML 

| Criterion        | Flask-WTF                                       | Pure WTForms                           | Manually with HTML                        |
|------------------|-------------------------------------------------|----------------------------------------|-------------------------------------------|
| Ease of use      | ✔️ High: Integrated with Flask. No need for setup | ❌ Medium: setup required               | ❌ Low: manual setup                       |
| Validation       | ✔️ Built-in validators, CSRF protection         | ✔️ validators are built-in              | ❌ Manual validation required              |
| Security         | ✔️ CSRF protection Integrated by default        | ❌ No CSRF protection. Setup required   | ❌ Manual CSRF protection required         |
| Flexibility      | ✔️ High: very flexible and customizable         | ✔️ High: customizable                   | ✔️ High: Full control                     |
| Learning curve   | ✔️ Low: Good documentation, Flask integration   | ❌ Medium: Setup needed                 | ❌ High: Knowledge of HTML required and validation logic |

---

### 05: [Managing  with Flask_apscheduler] 

### Meta 

Status 

: **Decided**  

Updated : 28-Juli-2024 

### Problem statement 

We need a solution that allows us to easily update the number of bags in every offer in our web application. In this case we need to update the offers that have a standart number of bags to the main number and Furthermore we want to implement that in our flask App without a high resources usage.

### Decision 

We will use Flask-WTF for form handling in our Flask application for several reasons. Firstly, Flask-WTF simplifies the creation and management of forms with its easy-to-use syntax and integration with Flask, eliminating the need for additional setup and saving us time and effort. Additionally, Flask-WTF provides a wide range of built-in validators for user input, ensuring that input is correct and consistent. Moreover, CSRF protection is built-in by default, allowing us to save development time and, most importantly, reduce security risks. 

### Regarded options 

We regarded three alternative options: 

Flask-WTF,Pure WTForms or Manually with HTML 

| Criterion        | Flask-WTF                                       | Pure WTForms                           | Manually with HTML                        |
|------------------|-------------------------------------------------|----------------------------------------|-------------------------------------------|
| Ease of use      | ✔️ High: Integrated with Flask. No need for setup | ❌ Medium: setup required               | ❌ Low: manual setup                       |
| Validation       | ✔️ Built-in validators, CSRF protection         | ✔️ validators are built-in              | ❌ Manual validation required              |
| Security         | ✔️ CSRF protection Integrated by default        | ❌ No CSRF protection. Setup required   | ❌ Manual CSRF protection required         |
| Flexibility      | ✔️ High: very flexible and customizable         | ✔️ High: customizable                   | ✔️ High: Full control                     |
| Learning curve   | ✔️ Low: Good documentation, Flask integration   | ❌ Medium: Setup needed                 | ❌ High: Knowledge of HTML required and validation logic |
