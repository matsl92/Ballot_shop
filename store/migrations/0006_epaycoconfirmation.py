# Generated by Django 4.1.7 on 2023-03-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_link_transaccion_link_de_pago_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EpaycoConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField()),
            ],
        ),
    ]
