#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from DjangoAPI.java import start_java, stop_java

def main():  
    # Init de la JVM
    start_java()
    


    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAPI.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)



    # Kill de la JVM
    try:
        stop_java()
    except:
        print("Failed to stop the JVM")


if __name__ == '__main__':
    main()
