# Generated by Django 4.2.1 on 2023-05-13 09:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("support_signup", "0013_delete_supportroleshift"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Schedule",
        ),
    ]
