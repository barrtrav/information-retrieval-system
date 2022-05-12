#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os, re, sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        try:
            os.environ['runserver']
            match = re.compile('--database=(\w+)').match(sys.argv[-1])
            if match:
                os.environ['database'] = match.group(1)
            else: os.environ['database'] = 'corpus'
        except KeyError:
            os.environ['runserver'] = ''
        
        if len(sys.argv) > 2:
            execute_from_command_line(sys.argv[:-1])
        else:
            execute_from_command_line(sys.argv)
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
