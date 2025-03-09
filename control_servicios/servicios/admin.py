from django.contrib import admin
from .models import Servicio, Factura, TipoTramite, EstadoTramite, Proveedor, Contratacion, EstadoContratacion, SectorContratacion

admin.site.register(Servicio)
admin.site.register(Factura)
admin.site.register(TipoTramite)
admin.site.register(EstadoTramite)
admin.site.register(Proveedor)
admin.site.register(Contratacion)
admin.site.register(EstadoContratacion)
admin.site.register(SectorContratacion)
