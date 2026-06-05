import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'overclock_pc_shop.settings')

application = get_wsgi_application()

# Auto-run migrations and admin setup on startup (for free hosting without shell access)
try:
    from django.core.management import call_command
    call_command('migrate', '--run-syncdb', verbosity=0)
    call_command('setup_admin', verbosity=0)
except Exception as e:
    import logging
    logging.getLogger(__name__).warning(f'Startup commands failed: {e}')
