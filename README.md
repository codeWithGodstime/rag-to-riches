# Django REST Framework Authentication Boilerplate

## Motivation

This project was born out of frustration with the repetitive process of writing and customizing the default Django user model to achieve a common authentication flow in Django Rest Framework (DRF). In my experience, while Djoser is a popular package for handling authentication, I found it challenging to write tests for—especially when it came to the email verification part. Additionally, Djoser often contains routes that I simply didn’t need, making it less flexible for projects that require a more custom authentication solution.

I created this boilerplate as a foundation for any DRF-based application with a focus on **Test-Driven Development (TDD)**. This eliminates the need to reinvent the wheel each time, providing a clean, customizable starting point for common authentication needs like user registration, email verification, login, logout, and password reset—all while being easily extendable for project-specific requirements.

## Features

- **Custom User Model**: Fully customizable Django user model tailored for common authentication flows.
- **JWT Authentication**: Includes JSON Web Token (JWT) support for secure authentication and authorization.
- **Email Verification**: Simplified and test-friendly email verification process using Django’s built-in email capabilities.
- **Password Reset**: Secure password reset flow with token-based validation.
- **Comprehensive Test Suite**: Written with TDD principles to ensure all major authentication flows are covered with unit and integration tests.
- **Minimal Dependencies**: Avoids unnecessary packages and routes to keep the project lightweight and easy to extend.

## Installation

1. Clone the repository:

   ```git clone https://github.com/yourusername/drf-auth-boilerplate.git ```
   ```cd drf-auth-boilerplate```

2. Install the required dependencies:
    ```pip install -r requirements.txt```

3. Set up the environment variables:
    Create a .env file in the root directory and add the following:

    ```
    SECRET_KEY=your-secret-key
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.your-email-provider.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@example.com
    EMAIL_HOST_PASSWORD=your-email-password
    ```
4. Apply the database migrations:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the development server:
    ```python manage.py runserver```

## Endpoints
```
Registration: /api/auth/register/
Login: /api/auth/login/
Logout: /api/auth/logout/
Email Verification: /api/auth/verify-email/
Password Reset: /api/auth/password-reset/
Password Change: /api/auth/password-change/
```

## Usage
Registration and Email Verification
- Register a new user using the /api/auth/register/ endpoint.
- A verification email is sent to the user's email address.
- The user verifies their account by clicking the link in the email or using the /api/auth/verify-email/ endpoint.

Password Reset

- Request a password reset link via the /api/auth/password-reset/ endpoint.
- The user receives an email with a link to reset their password.
- The password is updated using the token sent via email.

## Testing
This project is built with Test-Driven Development (TDD) in mind. Each major authentication feature has corresponding unit and integration tests. To run the test suite:


```
pytest
```

Tests include:

- User registration and login
- Email verification flow
- Password reset functionality
- JWT authentication and authorization

## Customization
This boilerplate is designed to be easily customizable. You can extend or modify the authentication flow as needed by overriding views, serializers, or models. The goal is to provide a flexible starting point without unnecessary features or routes that may not be needed in every project.

## Contributing
Contributions are welcome! Please fork the repository, create a new branch for your feature or bugfix, and submit a pull request.