import shutil
import sys
import tempfile
from pathlib import Path

import django
from django.conf import settings
from django.core.management import call_command


ROOT = Path(tempfile.mkdtemp(prefix="djux_auth_tests_"))
PACKAGE_ROOT = ROOT / "auth"
shutil.copytree(Path(__file__).resolve().parents[1] / "app", PACKAGE_ROOT)
sys.path.insert(0, str(ROOT))

if not settings.configured:
    settings.configure(
        SECRET_KEY="tests",
        ROOT_URLCONF="tests.urls",
        USE_TZ=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "rest_framework",
            "rest_framework_simplejwt.token_blacklist",
            "auth",
        ],
        MIDDLEWARE=[],
        PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        AUTH_USER_MODEL="auth_app.User",
        REST_FRAMEWORK={
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "rest_framework_simplejwt.authentication.JWTAuthentication",
            ]
        },
    )

django.setup()
call_command("migrate", verbosity=0, interactive=False)
