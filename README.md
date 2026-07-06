# Djux App: Auth

JWT authentication app for Djux projects. It provides registration, login,
refresh, logout, and authenticated profile endpoints.

## Install

Add the auth app and Simple JWT dependencies to `INSTALLED_APPS`, include
`auth.urls`, and run migrations.

```python
INSTALLED_APPS += [
    "auth",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

urlpatterns += [path("api/auth/", include("auth.urls"))]
AUTH_USER_MODEL = "auth_app.User"
```

## API

- `POST /api/auth/register/` - create a user and return JWT tokens
- `POST /api/auth/login/` - exchange credentials for JWT tokens
- `POST /api/auth/refresh/` - refresh an access token
- `POST /api/auth/logout/` - blacklist a refresh token
- `GET /api/auth/me/` - return the authenticated user
