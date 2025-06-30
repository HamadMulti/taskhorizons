# TaskHorizons

**TaskHorizons** is a modern, full-featured task and project management platform built with **Django** and **TailwindCSS**. It offers seamless user authentication, robust task tracking, productivity analytics, and an intuitive UI—all designed for teams and individuals who want to get things done efficiently.

## Project Structure
```bash
taskhorizons/
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── middleware.py
│   ├── models.py
│   ├── templatetags
│   │   └── custom_filters.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── dashboard
│   ├── apps.py
│   ├── __init__.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── Dockerfile
├── .dockerignore
├── .env
├── frontend
│   ├── apps.py
│   ├── __init__.py
│   ├── static_src
│   │   ├── .gitignore
│   │   ├── package.json
│   │   ├── package-lock.json
│   │   ├── postcss.config.js
│   │   ├── src
│   │   │   └── styles.css
│   │   └── tailwind.config.js
│   └── templates
│       ├── auth
│       │   ├── enable_email_otp.html
│       │   ├── login.html
│       │   ├── onboarding
│       │   │   ├── onboarding_base.html
│       │   │   ├── onboarding_complete.html
│       │   │   ├── step_1.html
│       │   │   ├── step_2.html
│       │   │   ├── step_3.html
│       │   │   └── step_4.html
│       │   ├── password_reset_complete.html
│       │   ├── password_reset_confirm.html
│       │   ├── password_reset_done.html
│       │   ├── password_reset.html
│       │   ├── profile.html
│       │   ├── profile_modal.html
│       │   ├── qr_code_modal.html
│       │   ├── register.html
│       │   ├── verify_email_otp.html
│       │   └── verify_totp_otp.html
│       ├── base.html
│       ├── _base_two.html
│       ├── breadcrumb.html
│       ├── dashboard
│       │   ├── dashboard.html
│       │   └── index.html
│       ├── dashboard_base.html
│       ├── footer.html
│       ├── landing
│       │   ├── cta.html
│       │   ├── features.html
│       │   ├── hero.html
│       │   ├── home.html
│       │   └── testimonials.html
│       ├── nav.html
│       ├── navigation.html
│       ├── projects
│       │   ├── project_confirm_delete.html
│       │   ├── project_form.html
│       │   └── project_list.html
│       ├── registration
│       │   └── password_reset_email.html
│       ├── tasks
│       │   ├── task_confirm_delete.html
│       │   ├── task_detail.html
│       │   ├── task_form.html
│       │   └── task_list.html
│       └── two_factor
│           └── _base.html
├── .gitignore
├── landing
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media
│   └── profile_pictures
├── project
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── README.md
├── requirements.txt
├── settings
│   ├── asgi.py
│   ├── context_processors.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── task
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── webhook.log
```

## Features

* **User Authentication**

  * Login, Registration, Password Reset
  * Two-Factor Authentication (Email & TOTP)
  * Profile Management

* **Task & Project Management**

  * Create, assign, update and delete tasks/projects
  * User-based task filtering
  * Deadlines, descriptions, and status tracking

* **Analytics Dashboard**

  * Visualize productivity
  * Track total/completed/pending tasks
  * Admin-level user performance insights

* **Landing Pages**

  * Hero section, testimonials, features, and call-to-action

* **Frontend**

  * Built using **TailwindCSS**
  * Responsive, modern, and accessible design

## ⚙️ Tech Stack

* **Backend:** Django 4+, SQLite3 (default), Django ORM
* **Frontend:** TailwindCSS, Django Templates
* **Auth:** Django built-in auth, 2FA via email and QR
* **Deployment Ready:** Dockerized

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/taskhorizons.git
cd taskhorizons
```

### Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### TailwindCSS Setup

Go to:

```bash
cd frontend/static_src
npm install
npm run build
```

This compiles the Tailwind styles to `frontend/static/`.

### Set Environment Variables

Create a `.env` file:

```ini
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Migrate DB and Create Superuser

```bash
python manage.py makemigrations django_otp
python manage.py migrate
python manage.py createsuperuser
```

### Run the App

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## Docker Setup (Optional)

```bash
docker build -t taskhorizons .
docker run -p 8000:8000 taskhorizons
```

## Testing

Run Django's built-in tests:

```bash
python manage.py test
```

## Media & Static Files

Make sure `media/` is writeable:

```bash
mkdir -p media/profile_pictures
chmod -R 755 media/
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License. See `LICENSE` file for details.

## Credits

Made with ❤️ using Django + TailwindCSS by \[HamadMulti].