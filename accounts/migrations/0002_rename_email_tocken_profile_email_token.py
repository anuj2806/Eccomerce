# Generated by Django 5.0 on 2023-12-24 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email_tocken',
            new_name='email_token',
        ),
    ]