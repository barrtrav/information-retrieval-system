#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


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
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    Path('../resource/').mkdir(exist_ok=True)
    Path('../resource/model/').mkdir(exist_ok=True)
    Path('../resource/corpus/').mkdir(exist_ok=True)
    Path('../resource/cluster/').mkdir(exist_ok=True)
    Path('../resource/recommend/').mkdir(exist_ok=True)
    Path('../resource/queries/').mkdir(exist_ok=True)
    Path('../resource/expansion/').mkdir(exist_ok=True)

    main()
