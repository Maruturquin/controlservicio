from django.contrib import admin
from django.urls import path
from servicios import views
from servicios.views import resumen_servicios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', resumen_servicios, name='resumen_servicios'),  # Raíz del sitio

    path('servicios/', views.servicio_list, name='servicio_list'),
    path('servicios/new/', views.servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/edit/', views.servicio_update, name='servicio_update'),
    path('servicios/<int:pk>/delete/', views.servicio_delete, name='servicio_delete'),
    path('tipo_tramite/', views.tipo_tramite_list, name='tipo_tramite_list'),
    path('tipo_tramite/new/', views.tipo_tramite_create, name='tipo_tramite_create'),
    path('tipo_tramite/<int:pk>/edit/', views.tipo_tramite_update, name='tipo_tramite_update'),
    path('tipo_tramite/<int:pk>/delete/', views.tipo_tramite_delete, name='tipo_tramite_delete'),
    path('estado_tramite/', views.estado_tramite_list, name='estado_tramite_list'),
    path('estado_tramite/new/', views.estado_tramite_create, name='estado_tramite_create'),
    path('estado_tramite/<int:pk>/edit/', views.estado_tramite_update, name='estado_tramite_update'),
    path('estado_tramite/<int:pk>/delete/', views.estado_tramite_delete, name='estado_tramite_delete'),
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/new/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/edit/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/delete/', views.proveedor_delete, name='proveedor_delete'),
    path('nombreservicio/', views.nombreservicio_list, name='nombreservicio_list'),
    path('nombreservicio/new/', views.nombreservicio_create, name='nombreservicio_create'),
    path('nombreservicio/<int:pk>/edit/', views.nombreservicio_update, name='nombreservicio_update'),
    path('nombreservicio/<int:pk>/delete/', views.nombreservicio_delete, name='nombreservicio_delete'),
    path('contrataciones/', views.contratacion_list, name='contratacion_list'),
    path('contrataciones/new/', views.contratacion_create, name='contratacion_create'),
    path('contrataciones/<int:pk>/edit/', views.contratacion_update, name='contratacion_update'),
    path('contrataciones/<int:pk>/delete/', views.contratacion_delete, name='contratacion_delete'),
    path('estado_contratacion/', views.estado_contratacion_list, name='estado_contratacion_list'),
    path('estado_contratacion/new/', views.estado_contratacion_create, name='estado_contratacion_create'),
    path('estado_contratacion/<int:pk>/edit/', views.estado_contratacion_update, name='estado_contratacion_update'),
    path('estado_contratacion/<int:pk>/delete/', views.estado_contratacion_delete, name='estado_contratacion_delete'),
    path('sector_contratacion/', views.sector_contratacion_list, name='sector_contratacion_list'),
    path('sector_contratacion/new/', views.sector_contratacion_create, name='sector_contratacion_create'),
    path('sector_contratacion/<int:pk>/edit/', views.sector_contratacion_update, name='sector_contratacion_update'),
    path('sector_contratacion/<int:pk>/delete/', views.sector_contratacion_delete, name='sector_contratacion_delete'),
    path('marcar_pagado/', views.marcar_pagado, name='marcar_pagado'),
    path('resumen/', resumen_servicios, name='resumen_servicios'),
    path('alertas/', views.alertas_list, name='alertas_list'),
]
