# Generated by Django 4.1.7 on 2023-03-17 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_rename_epaycoconfirmation_epaycolateconfirmation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='epaycolateconfirmation',
            name='post',
        ),
        migrations.AddField(
            model_name='epaycolateconfirmation',
            name='datos_json',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='epaycolateconfirmation',
            name='descripcion',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='epaycolateconfirmation',
            name='estado',
            field=models.IntegerField(choices=[(0, 'OK'), (1, 'Por resolver')], default=0),
        ),
        migrations.AddField(
            model_name='epaycolateconfirmation',
            name='transaccion',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.transaccion'),
        ),
    ]