## **PLEASE DO NOT USE REAL DATA, DEMO PURPOSES ONLY**

# ✅ VenTory: Full-Stack Inventory Management Application

---

# 📘 Project Overview

VenTory is a full-stack inventory management application developed to demonstrate my progression from creating websites into building complete web applications with a backend, database, authentication system, user roles, and structured application logic.

The purpose of the project is to provide a simple inventory management system for small businesses, allowing business owners and employees to manage stock, maintain user accounts, and keep track of important business activity.

The application allows users to register a business, create employee accounts, manage stock items, update account information, and maintain an activity log of important actions.

This project is built for **portfolio and educational purposes only**. It is a demonstration application and **is not intended to be used for a real business or with genuine business, employee, customer, financial, or other sensitive information**.

The main purpose behind VenTory was to gain experience building a larger Flask application and to understand how authentication, databases, user permissions, validation, security, file uploads, and application services work together.

---

# 🚀 Development Journey

VenTory represents another stage in my development journey because it moves beyond a simple website and into a more complete application with multiple connected systems.

The project was designed around a realistic business scenario where different users have different responsibilities.

While building VenTory, I worked with concepts including:

* Creating and managing a relational database.
* Connecting database models through relationships.
* Building authentication and user sessions.
* Creating different user roles and permissions.
* Hashing and verifying passwords.
* Validating user input.
* Managing stock and inventory information.
* Recording business activity.
* Uploading images using an external service.
* Protecting forms against CSRF attacks.
* Adding request rate limiting.
* Structuring backend logic into separate service modules.

The project also gave me experience working with a larger codebase where different parts of the application need to communicate with one another.

Rather than keeping all of the application logic inside `app.py`, functionality is separated into different services for areas such as authentication, users, stock, businesses, logging, configuration, and validation.

This makes the project easier to understand and provides a better foundation for continuing to develop it.

---

# ✨ Features

## 🏢 Business Registration

A new business owner can create a VenTory account by providing:

* Business name.
* Business address.
* Business telephone number.
* Business email address.
* Owner details.
* Owner email address.
* Password.

When registration is completed, a business and owner account are created in the database.

A username is automatically generated for the new owner.

The application also creates an initial daily password for the business.

---

## 👤 User Accounts

VenTory includes an authentication system allowing users to:

* Log in.
* Log out.
* Change their password.
* Reset their password using the business daily password.
* Update their personal details.
* Update business details where permitted.
* Access pages according to their role.

Passwords are hashed before being stored in the database rather than being stored as plain text.

---

## 👥 User Roles

VenTory uses three user roles:

* **Owner**
* **Manager**
* **Employee**

Different roles have different responsibilities within the application.

### Owner

Owners can:

* Manage their business details.
* Add employees and managers.
* View employees.
* View individual employee information.
* View employee activity logs.
* Remove employees.
* Reset employee passwords.
* Manage stock.

### Manager

Managers can:

* View stock.
* Add stock.
* Update stock.
* Delete stock.

### Employee

Employees can:

* View stock.
* Add stock.
* Update stock.

The intention is for stock management to be available to all employees, while more sensitive administrative actions remain restricted to appropriate roles.

---

## 📦 Stock Management

VenTory provides functionality for managing business inventory.

Users can add stock containing information such as:

* Product title.
* Description.
* Quantity.
* Supplier.
* Price.
* Product image.

Stock can then be viewed and searched through the inventory section.

Stock information can also be updated, including:

* Product title.
* Description.
* Supplier.
* Available quantity.
* Returned quantity.
* Damaged quantity.
* Price.
* Product image.

Stock items can also be removed by authorised users.

---

## 🔎 Stock Search

The inventory section includes a basic search function allowing users to search stock by product title.

This makes it easier to locate individual stock items when a business has multiple products stored in the system.

---

## 📊 Dashboard

The dashboard provides an overview of the business inventory.

Depending on the user's role, the dashboard calculates information including:

* Total stock.
* Total stock value.
* Returned stock.
* Returned stock value.
* Damaged stock.
* Damaged stock value.

This gives users a quick overview of the current inventory information.

---

## 📝 Business Activity Logs

VenTory records important actions performed within the application.

Examples include:

* User logins.
* User logouts.
* New account creation.
* Employee creation.
* Employee deletion.
* Password resets.
* Stock creation.
* Stock updates.
* Stock deletion.
* Profile changes.

Owners can view the overall business activity and can also view logs associated with individual employees.

The logs include information such as the user responsible for the action, the business, timestamp, and description of the activity.

---

## 🔐 Password Management

VenTory uses Argon2 password hashing to protect user passwords.

Users can change their password through their account settings.

The application also includes a daily password system which can be used to reset an account when required.

When an administrator resets a user's password, the account is marked as requiring a password change when the user next logs in.

---

## 🖼️ Image Uploads

VenTory supports image uploads for:

* Business logos.
* Stock item images.

Images are uploaded to Cloudinary rather than being stored directly inside the application's local filesystem.

The returned secure image URL is then stored in the database.

---

# 🏗️ Application Architecture

VenTory follows a structured Flask application design where different parts of the backend have separate responsibilities.

```text
VenTory/
│
├── app.py                         # Main Flask application and route handling
├── README.md                      # Project documentation
├── LICENSE                        # Project licence
│
├── database/
│   ├── __init__.py
│   ├── db.py                      # Database configuration
│   │
│   └── models/
│       ├── __init__.py
│       ├── business.py            # Business database model
│       ├── log.py                 # Activity log database model
│       ├── stock.py               # Stock database model
│       └── user.py                # User database model
│
├── services/
│   ├── __init__.py
│   ├── auth.py                    # Authentication and password functions
│   ├── businesses.py              # Business registration logic
│   ├── config.py                  # Configuration and image uploads
│   ├── log.py                     # Activity logging
│   ├── stock.py                   # Stock management logic
│   ├── users.py                   # User management logic
│   └── validators.py              # Input validation
│
├── templates/
│   ├── layout.html                # Base application layout
│   │
│   └── pages/
│       ├── admin/                 # Administrative pages
│       ├── error/                 # Error pages
│       ├── header-footer/         # Shared page components
│       ├── main/                  # Public pages
│       └── user-pages/            # Authenticated user pages
│
├── static/
│   ├── css/                       # Application styling
│   ├── js/                        # Client-side JavaScript
│   └── media/                     # Images and other media
│
├── instance/
│   └── ventory.db                 # SQLite database
│
└── .env                           # Environment variables (not included; see below)
```

---

## 🔐 Creating the `.env` File

VenTory requires a `.env` file in the root directory when running locally.

### ☁️ Cloudinary

Cloudinary is used to upload business logos and stock images.

Create a Cloudinary account or sign in to an existing one and obtain your API credentials.

Add the following to `.env`:

```env
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_URL=cloudinary://
```

Cloudinary images are not currently deleted when a stock item is removed from VenTory, so unused images may need to be removed manually from your Cloudinary account.

### 🔑 Secret Key

Flask requires a secret key for session management.

Generate one using Python:

```python
import secrets

secret = secrets.token_hex(32)

print(secret)
```

Then add the generated value to `.env`:

```env
SECRET_KEY=your_generated_secret_key
```

Your `.env` file should therefore contain:

```env
SECRET_KEY=your_generated_secret_key

CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_URL=cloudinary://
```

**Do not commit your `.env` file or its credentials to GitHub.**


# ⚙️ How The Application Works

## Flask Application (`app.py`)

`app.py` acts as the main entry point for the application.

It is responsible for:

* Creating the Flask application.
* Configuring the application.
* Registering sessions.
* Initialising the database.
* Enabling CSRF protection.
* Enabling request rate limiting.
* Defining application routes.
* Handling application errors.
* Adding security headers.

Routes receive requests from the frontend and then communicate with the appropriate service functions.

For example:

```python
@app.route("/user/add-new-stock", methods=["GET", "POST"])
```

handles requests for adding new stock.

The route receives the form information and passes the stock information to the stock service.

---

# 🗄️ Database

VenTory uses SQLite with SQLAlchemy as its ORM.

The database contains four main models:

```text
Business
   │
   ├── Users
   │
   ├── Stock
   │
   └── Logs
```

The relationships between these models allow information to be associated with the correct business and users.

---

## 🏢 Business Model

The business table stores information including:

* Business ID.
* Business name.
* Address.
* Telephone number.
* Email address.
* Logo URL.
* Daily password.
* Creation date.
* Update date.
* Daily password update date.

---

## 👤 User Model

The user table stores:

* User ID.
* Business ID.
* Username.
* Title.
* First name.
* Last name.
* Role.
* Email address.
* Password hash.
* Creation date.
* Update date.
* Password reset status.

Each user belongs to a business.

---

## 📦 Stock Model

The stock table stores:

* Stock ID.
* Business ID.
* Product title.
* Description.
* Price.
* Supplier.
* Image URL.
* Available quantity.
* Returned quantity.
* Damaged quantity.
* Total quantity.
* Creation date.
* Update date.

Each stock item belongs to a business.

---

## 📝 Log Model

The log table stores:

* Log ID.
* User ID.
* Business ID.
* Timestamp.
* Action description.

This allows important actions within a business to be recorded.

---

# 🧩 Services

VenTory separates much of its backend logic into service files.

## `auth.py`

Handles authentication-related functionality such as:

* Login authentication.
* Password hashing.
* Password verification.
* Session protection decorators.
* Username generation.
* Daily password generation.
* Daily password updates.

---

## `businesses.py`

Handles business registration.

The registration process validates the supplied information before creating the business and its initial owner account.

---

## `users.py`

Handles user-related operations including:

* Creating employees.
* Updating passwords.
* Updating account information.
* Removing users.
* Forgotten password functionality.

---

## `stock.py`

Handles stock-related operations including:

* Adding stock.
* Updating stock.
* Deleting stock.
* Uploading stock images.
* Recording stock activity.

---

## `log.py`

Contains the functionality used to create business activity records.

Keeping logging in its own service means different parts of the application can record activity without duplicating the database logic.

---

## `validators.py`

Contains the application's input validation functions.

Different validation rules are used for information such as:

* Email addresses.
* Telephone numbers.
* Passwords.
* Usernames.
* Prices.
* Numerical values.
* Dates.
* User roles.
* Titles.
* Addresses.

The intention is to validate information before it is used by the application's services or database.

---

# 🛡️ Security Implementation

Security was an important part of the project because VenTory handles user accounts, passwords, business information, and inventory data.

Although this application is intended only for demonstration purposes, I wanted to gain experience implementing some of the security practices used in web applications.

## Password Protection

Passwords are not stored as plain text.

VenTory uses:

* Argon2 password hashing.
* Password verification.
* Password reset handling.
* Password change functionality.

This helps prevent stored passwords from being directly readable if database information is exposed.

---

## Session Security

The application uses Flask-Session for managing authenticated user sessions.

Session configuration includes:

* HTTP-only cookies.
* Secure cookies.
* SameSite cookie restrictions.
* Session lifetime limits.
* Session clearing during authentication changes.

Protected routes also use authentication decorators to prevent unauthorised access.

---

## CSRF Protection

VenTory uses Flask-WTF's CSRF protection.

This helps protect form submissions against Cross-Site Request Forgery attacks.

CSRF protection is particularly relevant for actions which change application data, such as:

* Updating account details.
* Adding stock.
* Updating stock.
* Deleting stock.
* Adding employees.
* Removing employees.
* Changing passwords.

---

## Rate Limiting

Flask-Limiter is used to limit certain requests.

For example, limits are applied to areas such as:

* Login attempts.
* Registration attempts.
* Password-related actions.
* Employee creation.
* Other sensitive POST requests.

This helps reduce the risk of excessive automated requests against sensitive endpoints.

---

## Security Headers

The application also sets a Content Security Policy through an `after_request` handler.

The policy restricts where scripts, styles, fonts, and images can be loaded from.

This provides an additional layer of browser-side security.

---

## Input Validation

User input is passed through validation functions before being used by the application's services.

The validation system checks different types of information depending on the field.

This includes checking:

* Length.
* Format.
* Allowed characters.
* Numerical values.
* Email addresses.
* Telephone numbers.
* Password requirements.
* User roles.

---

# 🧩 Technology Stack

| Technology        | Purpose                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------- |
| **Python**        | Backend programming language used to build the application logic.                        |
| **Flask**         | Web framework handling routes, requests, templates, sessions, and application structure. |
| **SQLite**        | Database engine used to store businesses, users, stock, and activity logs.               |
| **SQLAlchemy**    | ORM used to define database models and interact with the database.                       |
| **Jinja**         | Server-side templating engine used to generate HTML pages dynamically.                   |
| **HTML5**         | Provides the structure and content of the application pages.                             |
| **CSS3**          | Handles application styling, layouts, and responsive presentation.                       |
| **JavaScript**    | Provides client-side functionality and interaction.                                      |
| **Argon2**        | Password hashing algorithm used to protect user credentials.                             |
| **Flask-Session** | Handles server-side session management.                                                  |
| **Flask-WTF**     | Provides CSRF protection.                                                                |
| **Flask-Limiter** | Provides request rate limiting.                                                          |
| **Cloudinary**    | External image hosting service used for business and stock images.                       |
| **python-dotenv** | Loads environment variables from the `.env` file.                                        |

---

# 🗄️ Database Design

VenTory uses four main database tables.

### Businesses Table

Stores business information.

* business_id
* business_name
* address
* telephone
* email
* logo_url
* daily_password
* created
* updated
* daily_password_updated

### Users Table

Stores user account information.

* user_id
* business_id
* username
* title
* first_name
* last_name
* role
* email
* password
* created
* updated
* password_reset

### Stock Table

Stores inventory information.

* stock_id
* business_id
* title
* description
* price
* supplier
* image_url
* returned
* damaged
* total
* available
* updated
* created

### Logs Table

Stores business activity.

* log_id
* user_id
* business_id
* timestamp
* comment

---

# 🖥️ How To Use The Application

VenTory is designed to be relatively straightforward to use.

## 1. Start The Application

Once the application has been installed and started, open it in a web browser.

The home page provides access to the main public sections of the application.

---

## 2. Register A Business

Select the registration option.

Enter the requested business and owner information.

The registration process creates:

* A new business.
* An owner account.
* A generated username.
* A business daily password.

The generated username should be kept somewhere safe for the demonstration.

---

## 3. Log In

Use the generated username and the password entered during registration.

After successful authentication, you will be taken to the dashboard.

---

## 4. Use The Dashboard

The dashboard provides an overview of the business and its stock.

Depending on the account role, additional management options will be available.

---

## 5. Add Stock

Navigate to the stock section and select the option to add new stock.

Enter the product information, including:

* Title.
* Quantity.
* Supplier.
* Description.
* Price.
* Optional image.

Once submitted, the stock will be added to the business inventory.

---

## 6. Manage Stock

Users with access to stock management can view the inventory and search for products.

Selecting a stock item allows its information to be updated.

Changes to stock are recorded in the business activity logs.

---

## 7. Manage Employees

Business owners can create new employee or manager accounts.

When creating an account, VenTory generates:

* A username.
* A temporary password.

The generated login details should be provided to the new user for the purposes of the demonstration.

Owners can also view employee information, review employee activity, reset passwords, and remove employee accounts.

---

## 8. View Business Activity

Owners can access the business activity section to view actions recorded by the application.

The activity page can also be filtered by date.

This provides a basic history of activity taking place within the business.

---

# ⚠️ Demo Application Notice

VenTory is **not a real business management system**.

The application has been created for **portfolio, learning, and demonstration purposes only**.

Please **do not enter real information**, including:

* Real business details.
* Real employee information.
* Real customer information.
* Real passwords.
* Real financial information.
* Confidential stock information.
* Any other sensitive information.

The application should be treated as a demonstration of development skills rather than a production-ready business management platform.

---

# 📋 Requirements

* Python 3.10+
* pip
* Virtual environment
* Cloudinary account for image uploads

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd inventory-manager
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create the environment variables required by the application:

```text
SECRET_KEY=your_secret_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

The application also contains configuration which can generate the `SECRET_KEY` environment variable when required.

Start the application:

```bash
flask run
```

The application can then be opened in a web browser using the local Flask address.

---

# ☁️ Image Uploads

VenTory uses Cloudinary to store uploaded images.

A Cloudinary account is therefore required if you want to test the image upload functionality.

The application uploads images into folders associated with the business and the type of image being uploaded.

For example:

```text
VenTory-portfolio-project/
│
└── Business Name/
    ├── logo/
    └── stock-items/
```

The secure URL returned by Cloudinary is then stored in the database.

---

# 🔮 Future Improvements

There are several areas that could be improved as the project continues to develop.

Possible future improvements include:

* Adding automated tests.
* Improving database transactions.
* Adding database migrations.
* Further improving session security.
* Improving role and permission handling.
* Adding more detailed stock reporting.
* Adding stock categories.
* Adding stock thresholds and low-stock notifications.
* Improving inventory calculations.
* Adding pagination for larger inventories.
* Improving search and filtering.
* Adding better error handling and logging.
* Migrating from SQLite to PostgreSQL for larger deployments.
* Improving accessibility.
* Improving the frontend experience.
* Adding a proper production deployment configuration.
* Refactoring some application services as the project grows.

These improvements would help move the application from a learning and portfolio project towards a more production-oriented application.

---

## 📄 Licence

<p>
  This project is licensed under the <b>MIT Licence</b> — see the <a href="./LICENCE">LICENCE</a> file for details.
</p>

<pre>
MIT Licence

Copyright (c) 2026 Sheikh Hussain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</pre>

---

## Footnote

<div align="center" style="border: 1px solid green; padding: 10px; border-radius: 5px;">
  <p>🗣️ Feel free to follow, connect, and chat!</p>
  <a class="header-badge" target="_blank" href="https://github.com/Sheikh-H"><img src="https://img.shields.io/badge/GitHub-376e00?style=flat&logo=github&logoColor=white" alt="GitHub"></a>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/sheikh-hussain/"><img src="https://img.shields.io/badge/LinkedIn-376e00?style=flat&logo=LinkedIn&logoColor=white" alt="LinkedIn"></a>
  <a class="header-badge" target="_blank" href="mailto:sheikh.hussain1155@gmail.com"><img src="https://img.shields.io/badge/Gmail-376e00?style=flat&logo=gmail&logoColor=white" alt="Gmail"></a>
  <a class="header-badge" target="_blank" href="https://sheikh-hussain.onrender.com/"><img src="https://img.shields.io/badge/Portfolio-376e00?style=flat&logo=github&logoColor=white" alt="Portfolio"></a>
</div>

<div align="center">
  <a href="https://sheikh-hussain.onrender.com/" target="_blank">By Sheikh Hussain 💚</a>
</div>


**Please do not use real data. Demo purposes only.**
