## **PLEASE DO NOT USE REAL DATA, DEMO PURPOSES ONLY**

# ✅ VenTory: Full-Stack Inventory Management Application

**VenTory is an educational portfolio project created for learning and development purposes. It is not a commercial product or service.**

This is a personal educational/demo project created for portfolio and learning purposes. The project is not operated as a commercial service. If the name or any other branding used in this project conflicts with an existing trademark or intellectual property right, please let me know and I will review and, where appropriate, change it.
---

# 📘 Project Overview

VenTory is a full-stack inventory management application developed to demonstrate my progression from creating websites into building complete web applications with a backend, database, authentication system, user roles, validation, security controls, and structured application logic.

The purpose of the project is to provide a simple inventory management system for small businesses, allowing business owners and employees to manage stock, maintain user accounts, and keep track of important business activity.

The application allows users to register a business, create employee accounts, manage stock items, update account information, and maintain activity logs of important actions.

**VenTory is a demonstration and portfolio project only. It is not a production-ready business management system and must not be used with real business, employee, customer, financial, personal, confidential, or otherwise sensitive information.**

The application may be deployed using temporary hosting and storage for demonstration purposes. Data stored in a deployed demonstration environment should therefore be considered temporary and should never be treated as persistent or secure business storage.

The main purpose behind VenTory was to gain experience building a larger Flask application and to understand how authentication, databases, user permissions, validation, security, file uploads, logging, and application services work together.

---

# 🚀 Development Journey

VenTory represents another stage in my development journey because it moves beyond a simple website and into a more complete application with multiple connected systems.

The project was designed around a realistic business scenario where different users have different responsibilities.

While building VenTory, I worked with concepts including:

* Creating and managing a relational database.
* Connecting database models through relationships.
* Building authentication and user sessions.
* Creating different user roles and permissions.
* Hashing and verifying passwords using Argon2.
* Validating user input.
* Managing stock and inventory information.
* Recording business activity.
* Uploading images using an external service.
* Protecting forms against CSRF attacks.
* Adding request rate limiting.
* Structuring backend logic into separate service modules.
* Handling database transactions and rollbacks.
* Implementing role-based access controls.
* Working with environment variables and application configuration.

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

The supplied information is validated before the registration process continues.

When registration is completed, a business and owner account are created in the database.

A username is automatically generated for the new owner.

The registration process explicitly creates the initial account with the **owner** role rather than relying on the submitted role value.

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

Users who have been given a temporary or reset password can be required to change their password through the application's password-reset process.

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
* Add managers and employees.
* View employees.
* View individual employee information.
* View employee activity logs.
* Remove non-owner users.
* Reset employee passwords.
* Manage stock.
* View business activity logs.
* View business inventory information.

### Manager

Managers can:

* View stock.
* Add stock.
* Update stock.
* Manage inventory within the permissions provided by the application.
* Manage employee-related functions where authorised by the application.

### Employee

Employees can:

* View stock.
* Add stock.
* Update stock.
* Manage inventory within the permissions provided by the application.

The intention is for more sensitive administrative actions, such as managing users and business-level information, to remain restricted to appropriate roles.

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

Authorised users can also remove stock items.

Stock-related actions are recorded in the business activity logs.

---

## 🔎 Stock Search

The inventory section includes a basic search function allowing users to search stock by product information.

This makes it easier to locate individual stock items when a business has multiple products stored in the system.

---

## 📊 Dashboard

The dashboard provides an overview of the business inventory.

Depending on the user's role, the dashboard displays information including:

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
* New business and owner account creation.
* Employee creation.
* Employee deletion.
* Password resets.
* Stock creation.
* Stock updates.
* Stock deletion.
* Profile changes.
* Business detail changes.

Owners can view the overall business activity and can also view logs associated with individual employees.

The logs include information such as the user responsible for the action, the business, timestamp, and description of the activity.

---

## 🔐 Password Management

VenTory uses **Argon2** password hashing to protect user passwords.

Users can change their password through their account settings.

The application also includes a daily password system which can be used to authenticate a password-reset request.

Daily passwords are generated for each business and periodically regenerated by the application.

When a password is reset, the relevant account is marked as requiring a password reset. The user can then use the appropriate reset process to establish a new password.

The daily password system is intended as a demonstration feature and should not be treated as a replacement for a production-grade password recovery system.

---

## 🖼️ Image Uploads

VenTory supports image uploads for:

* Business logos.
* Stock item images.

Images are uploaded to Cloudinary rather than being stored directly inside the application's local filesystem.

The returned secure image URL is then stored in the database.

Cloudinary images are not automatically deleted when a corresponding stock item is removed, meaning unused images may need to be removed manually from the Cloudinary account.

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
│   └── ventory.db                 # SQLite database used locally
│
└── .env                           # Environment variables (not included)
```

---

# 🔐 Creating the `.env` File

VenTory requires environment variables for configuration when running locally or in a deployment environment.

A `.env` file can be created in the root directory for local development.

**Do not commit your `.env` file or any credentials to GitHub.**

## ☁️ Cloudinary

Cloudinary is used to upload business logos and stock images.

Create a Cloudinary account or sign in to an existing one and obtain the required API credentials.

Add the following to `.env`:

```env
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_URL=your_cloudinary_url
```

Only include `CLOUDINARY_URL` if it is required by your local configuration.

Cloudinary images are not currently deleted automatically when a stock item is removed from VenTory, so unused images may need to be removed manually from your Cloudinary account.

---

## 🔑 Secret Key

Flask requires a secret key for secure session management.

A secret key can be generated using Python:

```python
import secrets

secret = secrets.token_hex(32)

print(secret)
```

Then add the generated value to `.env`:

```env
SECRET_KEY=your_generated_secret_key
```

Your local `.env` file should therefore contain the required configuration values:

```env
SECRET_KEY=your_generated_secret_key

CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_URL=your_cloudinary_url
```

**Never commit these values to GitHub.**

For a hosted deployment, configure these values through the hosting provider's environment-variable settings rather than uploading the `.env` file.

---

# ⚙️ How The Application Works

## Flask Application (`app.py`)

`app.py` acts as the main entry point for the application.

It is responsible for:

* Creating the Flask application.
* Configuring the application.
* Configuring sessions.
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

The route receives the form information and passes the stock information to the appropriate stock service.

---

# 🗄️ Database

VenTory uses **SQLite with SQLAlchemy** as its ORM.

The main database models are:

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

Business and user creation are handled within the same database transaction so that a failure during the process can be rolled back.

---

## `users.py`

Handles user-related operations including:

* Creating employees.
* Updating passwords.
* Updating account information.
* Removing users.
* Forgotten-password functionality.

User operations also include validation and role-based restrictions.

---

## `stock.py`

Handles stock-related operations including:

* Adding stock.
* Updating stock.
* Deleting stock.
* Uploading stock images.
* Recording stock activity.
* Managing inventory quantities.

---

## `log.py`

Contains the functionality used to create business activity records.

Keeping logging in its own service means different parts of the application can record activity without duplicating the database logic.

Important operations check whether log creation succeeds before committing the associated database changes where appropriate.

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
* General text fields.

The intention is to validate information before it is used by the application's services or database.

---

# 🛡️ Security Implementation

Security was an important part of the project because VenTory handles user accounts, passwords, business information, and inventory data.

Although this application is intended only for demonstration purposes, I wanted to gain experience implementing security practices commonly used in web applications.

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

Session configuration includes security-related cookie settings such as:

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

Validation is performed on the server side rather than relying solely on browser-side HTML validation.

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

The registration process validates the supplied information before creating:

* A new business.
* An owner account.
* A generated username.
* A business daily password.

The generated username should be kept somewhere safe for the purposes of the demonstration.

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
* Image.

Once submitted, the stock will be added to the business inventory.

---

## 6. Manage Stock

Users with access to stock management can view the inventory and search for products.

Selecting a stock item allows its information to be updated according to the user's permissions.

Changes to stock are recorded in the business activity logs.

---

## 7. Manage Employees

Business owners can create new employee or manager accounts.

When creating an account, VenTory generates:

* A username.
* A temporary password.

The generated login details should be provided to the new user for the purposes of the demonstration.

Owners can also view employee information, review employee activity, reset passwords, and remove non-owner accounts.

---

## 8. View Business Activity

Owners can access the business activity section to view actions recorded by the application.

The activity page can also be filtered by date.

This provides a basic history of activity taking place within the business.

---

# ⚠️ Demo Application Notice

VenTory is **not a real business management system**.

The application has been created for **portfolio, learning, and demonstration purposes only**.

### **DO NOT USE REAL DATA.**

Please **do not enter real or sensitive information**, including:

* Real business details.
* Real employee information.
* Real customer information.
* Real passwords.
* Real financial information.
* Confidential stock information.
* Personal information.
* API keys or other credentials.
* Any other sensitive information.

Any deployed demonstration environment should be treated as temporary and unsuitable for storing important or persistent data.

The application should be treated as a demonstration of development skills rather than a production-ready business management platform.

---

# 📋 Requirements

* Python 3.10+
* pip
* Virtual environment
* Cloudinary account for image uploads if image functionality is being tested

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd ventory-inventory-manager
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

Create the environment variables required by the application.

For local development, these can be stored in a `.env` file:

```text
SECRET_KEY=your_secret_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_URL=your_cloudinary_url
```

Only include `CLOUDINARY_URL` if it is required by your configuration.

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

Cloudinary-hosted images are separate from the local SQLite database. Removing a stock item from VenTory does not currently remove its corresponding Cloudinary image automatically.

---

# ☁️ Deployment

VenTory can be deployed as a demonstration application using a hosting service such as Render.

When deploying the application:

* Configure environment variables through the hosting provider.
* Do not upload the `.env` file.
* Do not expose API credentials.
* Configure the required Cloudinary credentials.
* Treat the deployed SQLite database as temporary unless persistent storage has specifically been configured.
* Do not use the deployed application to store real or sensitive information.

The deployed version exists primarily to allow the application to be demonstrated as part of a portfolio.

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
* Improving image lifecycle management by automatically removing unused Cloudinary images.
* Adding stronger password recovery mechanisms suitable for production applications.
* Further separating route handling from application and service logic as the project grows.

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
