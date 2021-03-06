# Generated by Django 3.0.3 on 2020-06-02 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200529_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
