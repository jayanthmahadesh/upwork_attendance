from django.contrib.auth.models import Group
from django.db import migrations
from django.apps import AppConfig


class RosterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roster'


def create_groups(apps, schema_editor):
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Staff')


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
