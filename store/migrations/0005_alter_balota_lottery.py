# Generated by Django 4.1.7 on 2023-04-06 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_lottery_date_rifa_lottery_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balota',
            name='lottery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.rifa', verbose_name='Rifa'),
        ),
    ]