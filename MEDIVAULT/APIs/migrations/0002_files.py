# Generated by Django 4.2.2 on 2023-06-26 10:41

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='files/')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APIs.individual')),
            ],
        ),
    ]
