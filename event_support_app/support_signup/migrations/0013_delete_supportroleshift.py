# Generated by Django 4.2.1 on 2023-05-13 08:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("support_signup", "0012_alter_participant_shifts_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SupportRoleShift",
        ),
    ]
