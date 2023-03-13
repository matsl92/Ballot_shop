# Generated by Django 4.1.7 on 2023-03-13 21:16

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_rango_alter_balota_precio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaccion',
            name='ref_epayco',
        ),
        migrations.AddField(
            model_name='transaccion',
            name='x_description',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaccion',
            name='x_ref_payco',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='balota',
            name='time_period',
            field=models.DurationField(default=datetime.timedelta(seconds=600)),
        ),
        migrations.AlterField(
            model_name='balota',
            name='transaccion',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='store.transaccion'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='cliente',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.cliente'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='descuento',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='store.descuento'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='link_de_pago',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='valid_until',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='valor_final',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='valor_inicial',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]