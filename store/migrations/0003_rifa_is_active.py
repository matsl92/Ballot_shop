# Generated by Django 4.1.7 on 2023-04-01 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cliente_email_alter_cliente_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rifa',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
