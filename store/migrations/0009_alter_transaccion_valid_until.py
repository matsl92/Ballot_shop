# Generated by Django 4.1.7 on 2023-03-05 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_transaccion_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='valid_until',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
