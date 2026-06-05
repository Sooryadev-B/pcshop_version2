#!/usr/bin/env python
"""
Startup script: runs migrate + setup_admin then launches gunicorn.
Set as Start Command on Render: python startup.py
"""
import os
import sys
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'overclock_pc_shop.settings')

import django
django.setup()

from django.core.management import call_command

print(">>> Running migrations...")
call_command('migrate', '--run-syncdb', verbosity=1)

print(">>> Setting up admin...")
call_command('setup_admin', verbosity=1)

print(">>> Starting gunicorn...")
os.execvp('gunicorn', ['gunicorn', 'overclock_pc_shop.wsgi'])
