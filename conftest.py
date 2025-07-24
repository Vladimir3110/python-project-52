import os

import pytest
from django.conf import settings
from django.core.management import call_command

from task_manager.statuses.models import Status


@pytest.fixture(autouse=True, scope="function")
def setup_statuses(db):
    if not Status.objects.exists():
        Status.objects.bulk_create([
            Status(name="Новый"),
            Status(name="В работе"),
            Status(name="Завершен")
        ])


def pytest_sessionstart(session):
    if not os.path.exists(settings.STATIC_ROOT):
        os.makedirs(settings.STATIC_ROOT)
    call_command('collectstatic', interactive=False, clear=True)
