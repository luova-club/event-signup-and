# Generated by Django 4.2.1 on 2023-05-08 16:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("support_signup", "0004_participantshift_role_supportroleshift_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="participantshift",
            unique_together={("participant", "shift")},
        ),
    ]