# Breathe_x

### Directory
```bash
├── access_control
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
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
│   └── views.py
├── content
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── management
│   │   └── commands
│   │       └── create_admin.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
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
│       ├── content
│       │   ├── category_list.html
│       │   ├── content.html
│       │   ├── dashboard.html
│       │   ├── locked.html
│       │   ├── no_questions.html
│       │   └── question.html
│       ├── dashboard_base.html
│       ├── footer.html
│       ├── landing
│       │   ├── contcatus.html
│       │   ├── cta.html
│       │   ├── features.html
│       │   ├── hero.html
│       │   ├── home.html
│       │   └── testimonials.html
│       ├── nav.html
│       ├── navigation.html
│       ├── payments
│       │   ├── initiate_payment.html
│       │   ├── payment_failure.html
│       │   ├── payment_result.html
│       │   ├── payment_success.html
│       │   └── transaction_list.html
│       ├── registration
│       │   └── password_reset_email.html
│       └── two_factor
│           └── _base.html
├── .gitignore
├── instasend_webhook.log
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
│       └── me-pic.jpg
├── mock_callback.json
├── payments
│   ├── admin.py
│   ├── apps.py
│   ├── celery.py
│   ├── forms.py
│   ├── __init__.py
│   ├── managment
│   │   └── commands
│   │       └── mpesa_test_stk_push.py
│   ├── models.py
│   ├── services.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
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
├── staticfiles
├── .vscode
│   └── settings.json
└── webhook.log
```
