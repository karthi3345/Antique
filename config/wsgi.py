"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information about deploying Django, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()


# --- Serverless bootstrap (Vercel) ---------------------------------------
# Vercel ignores buildCommand when a legacy `builds` array is present, so
# migrations and the collection seed run here, once per lambda cold start,
# guarded to be safe against concurrent instances and already-applied state.
def _bootstrap() -> None:
    if os.environ.get("VOLGO_BOOTSTRAPPED"):
        return
    os.environ["VOLGO_BOOTSTRAPPED"] = "1"
    if not os.environ.get("DATABASE_URL"):
        return  # nothing to do without a platform database
    try:
        from django.core.management import call_command
        call_command("migrate", interactive=False, verbosity=0)
        call_command("seed_volgo", verbosity=0)
    except Exception as exc:  # never block serving on bootstrap issues
        print(f"[wsgi] bootstrap skipped: {exc.__class__.__name__}: {exc}")


_bootstrap()
