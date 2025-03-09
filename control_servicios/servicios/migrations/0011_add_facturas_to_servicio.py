from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0010_servicio_monto_unitario_servicio_nro_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='facturas',
            field=models.ManyToManyField(related_name='servicio_set', to='servicios.Factura'),
        ),
    ]
