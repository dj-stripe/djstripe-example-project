from django.contrib.auth.models import User
from django.db import migrations


def forwards_func(apps, schema_editor):
    User.objects.create_superuser(
        username="admin", password="admin", email="admin@example.com"
    )


def reverse_func(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="admin").delete()


class Migration(migrations.Migration):
    dependencies = [("djstripe_example", "0001_initial")]
    operations = [migrations.RunPython(forwards_func, reverse_func)]
