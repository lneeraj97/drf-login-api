# Generated by Django 3.0.3 on 2020-06-02 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200602_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstatus',
            old_name='status',
            new_name='status_text',
        ),
    ]
