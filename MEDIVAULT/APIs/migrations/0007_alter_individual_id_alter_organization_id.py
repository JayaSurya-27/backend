# Generated by Django 4.2.2 on 2023-06-21 15:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0006_alter_individual_id_alter_organization_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]