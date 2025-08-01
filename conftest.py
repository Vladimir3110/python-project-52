import os

import pytest
from django.conf import settings

from task_manager.statuses.models import Status


@pytest.fixture(autouse=True, scope="function")
def setup_statuses(db):
    if not Status.objects.exists():
        Status.objects.bulk_create([
            Status(name="Новый"),
            Status(name="В работе"),
            Status(name="Завершен")
        ])


@pytest.fixture(autouse=True)
def setup_static(tmp_path):
    settings.STATIC_ROOT = tmp_path / 'staticfiles'
    os.makedirs(settings.STATIC_ROOT, exist_ok=True)
