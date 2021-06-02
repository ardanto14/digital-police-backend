#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv
from firebase_admin import credentials
import firebase_admin

def main():
    dotenv.read_dotenv()
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digitalpolice.settings')

    cred = credentials.Certificate('credentials.json')
    
    try:
        default_app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'bangkit-capstone-312901.appspot.com',
    })
    except ValueError:
        default_app = firebase_admin.get_app()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
