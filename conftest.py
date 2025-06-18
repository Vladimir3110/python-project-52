import pytest

from task_manager.statuses.models import Status


@pytest.fixture(autouse=True, scope="function")
def setup_statuses(db):
    print("Checking statuses...")
    if not Status.objects.exists():
        print("Creating statuses...")
        Status.objects.bulk_create([
            Status(name="Новый"),
            Status(name="В работе"),
            Status(name="Завершен")
        ])
    else:
        print("Statuses already exist")
