# Generated by Django 5.0.3 on 2024-04-03 21:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_alter_registroproducto_rrazon_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroproducto',
            name='rrazon',
            field=models.CharField(choices=[('Compra', 'Compra'), ('Expiró', 'Expiró'), ('Traslado', 'Traslado')], max_length=20),
        ),
        migrations.AlterField(
            model_name='ventageneral',
            name='tipo_comprobante',
            field=models.CharField(choices=[('Factura Electronica', 'Factura Electronica'), ('Boleta Electronica', 'Boleta Electronica')], max_length=100),
        ),
        migrations.CreateModel(
            name='RegistroAuditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
