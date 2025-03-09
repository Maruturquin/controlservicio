from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class NombreServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class TipoTramite(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class EstadoTramite(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    nro_factura = models.CharField(max_length=100)
    monto_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nro_factura} - {self.monto_unitario}"

class Servicio(models.Model):
    nombre = models.ForeignKey(NombreServicio, on_delete=models.CASCADE)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    expediente = models.CharField(max_length=100)
    # nro_factura = models.CharField(max_length=100)  # Removed
    # monto_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Removed
    detalle = models.TextField()
    tipo_tramite = models.ForeignKey(TipoTramite, on_delete=models.CASCADE)
    estado_tramite = models.ForeignKey(EstadoTramite, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    vencimiento = models.DateField(null=True, blank=True)
    fecha_inicio_tramite = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    duracion_tramite = models.IntegerField(null=True, blank=True)
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    @property
    def saldo_dias(self):
        contratacion = Contratacion.objects.filter(nombre=self.nombre).first()
        if contratacion:
            return contratacion.saldo_dias
        return None

    @property
    def monto_total(self):
        return sum(factura.monto_unitario for factura in self.factura_set.all())

    def save(self, *args, **kwargs):
        if self.fecha_pago:
            self.duracion_tramite = (self.fecha_pago - self.fecha_inicio_tramite).days
            try:
                self.estado_tramite = EstadoTramite.objects.get(nombre="Pagado")
            except ObjectDoesNotExist:
                pass  # Handle the case where "Pagado" does not exist
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre.nombre

class EstadoContratacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SectorContratacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Contratacion(models.Model):
    nombre = models.ForeignKey(NombreServicio, on_delete=models.CASCADE)
    nro_ultima_orden_compra = models.CharField(max_length=100)
    duracion_meses = models.IntegerField(editable=False, default=0)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    saldo_dias = models.IntegerField(editable=False, default=0)
    nro_expediente_contratacion = models.CharField(max_length=100)
    vigente = models.BooleanField(default=True)
    en_tramite = models.BooleanField(default=False)
    estado = models.ForeignKey(EstadoContratacion, on_delete=models.CASCADE)
    sector = models.ForeignKey(SectorContratacion, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.fecha_inicio and self.fecha_finalizacion:
            delta = self.fecha_finalizacion - self.fecha_inicio
            self.duracion_meses = delta.days // 30  # Approximate month calculation
        if self.fecha_finalizacion:
            self.saldo_dias = (self.fecha_finalizacion - timezone.now().date()).days
        super().save(*args, **kwargs)

    def is_near_expiration(self):
        if self.fecha_finalizacion:
            return (self.fecha_finalizacion - timezone.now().date()).days <= 90
        return False

    def __str__(self):
        return self.nombre.nombre
