#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djstripe_example.settings")

try:
    from django.core.management import call_command, execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. "
        "Run `poetry shell` to activate a virtual environment first."
    ) from exc


def main():
    execute_from_command_line(sys.argv)


def makemigrations():
    call_command("makemigrations")


def migrate():
    call_command("migrate")


def start():
    sys.argv[:] = ["manage.py", "runserver", *sys.argv[1:]]
    call_command("runserver")


def dev():
    start()


if __name__ == "__main__":
    main()
