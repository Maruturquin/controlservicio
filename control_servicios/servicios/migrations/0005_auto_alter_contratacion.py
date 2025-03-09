from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0004_contratacion_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contratacion',
            name='servicio',
        ),
        migrations.AlterField(
            model_name='contratacion',
            name='nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicios.nombreservicio'),
        ),
    ]
