from django.shortcuts import render, get_object_or_404, redirect
from .models import Servicio, Factura, TipoTramite, EstadoTramite, Proveedor, Contratacion, EstadoContratacion, SectorContratacion, NombreServicio
from .forms import EstadoTramiteForm, ServicioForm, FacturaForm, FacturaFormSet, ContratacionForm, TipoTramiteForm, ProveedorForm, NombreServicioForm, EstadoContratacionForm, SectorContratacionForm, PagoForm
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.urls import reverse

def servicio_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    servicios = Servicio.objects.all()

    if query:
        servicios = servicios.filter(
            Q(nombre__icontains=query) |
            Q(expediente__icontains=query) |
            Q(detalle__icontains=query) |
            Q(tipo_tramite__nombre__icontains=query) |
            Q(estado_tramite__nombre__icontains=query) |
            Q(proveedor__nombre__icontains=query)
        )

    if fecha_desde:
        servicios = servicios.filter(fecha_desde__gte=fecha_desde)
    if fecha_hasta:
        servicios = servicios.filter(fecha_hasta__lte=fecha_hasta)

    if direction == 'desc':
        order_by = f'-{order_by}'
    servicios = servicios.order_by(order_by)

    # Utilizamos `prefetch_related` para cargar las facturas asociadas con cada servicio
    servicios = servicios.prefetch_related('factura_set')

    paginator = Paginator(servicios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    alertas_count = Contratacion.objects.filter(fecha_finalizacion__lte=date.today() + timedelta(days=90)).count()

    return render(request, 'servicios/servicio_list.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'alertas_count': alertas_count,
    })


def servicio_create(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        formset = FacturaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            servicio = form.save()
            formset.instance = servicio
            formset.save()
            return redirect('servicio_list')
        else:
            print(form.errors, formset.errors)
    else:
        form = ServicioForm()
        formset = FacturaFormSet()
    return render(request, 'servicios/servicio_form.html', {'form': form, 'formset': formset})

def servicio_update(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        formset = FacturaFormSet(request.POST, instance=servicio)
        if form.is_valid() and formset.is_valid():
            servicio = form.save()
            formset.instance = servicio
            formset.save()
            return redirect('servicio_list')
        else:
            print(form.errors, formset.errors)
    else:
        form = ServicioForm(instance=servicio)
        formset = FacturaFormSet(instance=servicio)
    return render(request, 'servicios/servicio_form.html', {'form': form, 'formset': formset, 'servicio': servicio})

def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicio_list')
    return render(request, 'servicios/servicio_confirm_delete.html', {'servicio': servicio})

def tipo_tramite_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    tipos = TipoTramite.objects.all()

    if query:
        tipos = tipos.filter(
            Q(nombre__icontains=query)
        )

    if direction == 'desc':
        order_by = f'-{order_by}'
    tipos = tipos.order_by(order_by)

    paginator = Paginator(tipos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/tipo_tramite_list.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

def tipo_tramite_create(request):
    if request.method == 'POST':
        form = TipoTramiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_tramite_list')
    else:
        form = TipoTramiteForm()
    return render(request, 'servicios/tipo_tramite_form.html', {'form': form})

def tipo_tramite_update(request, pk):
    tipo_tramite = get_object_or_404(TipoTramite, pk=pk)
    if request.method == 'POST':
        form = TipoTramiteForm(request.POST, instance=tipo_tramite)
        if form.is_valid():
            form.save()
            return redirect('tipo_tramite_list')
    else:
        form = TipoTramiteForm(instance=tipo_tramite)
    return render(request, 'servicios/tipo_tramite_form.html', {'form': form, 'tipo_tramite': tipo_tramite})

def tipo_tramite_delete(request, pk):
    tipo_tramite = get_object_or_404(TipoTramite, pk=pk)
    if request.method == 'POST':
        tipo_tramite.delete()
        return redirect('tipo_tramite_list')
    return render(request, 'servicios/tipo_tramite_confirm_delete.html', {'tipo': tipo_tramite})

def estado_tramite_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    estados = EstadoTramite.objects.all()

    if query:
        estados = estados.filter(
            Q(nombre__icontains=query)
        )

    if direction == 'desc':
        order_by = f'-{order_by}'
    estados = estados.order_by(order_by)

    paginator = Paginator(estados, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/estado_tramite_list.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction,
        'estados': estados  # Asegúrate de pasar 'estados' al contexto
    })

def estado_tramite_create(request):
    if request.method == 'POST':
        form = EstadoTramiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estado_tramite_list')
    else:
        form = EstadoTramiteForm()
    return render(request, 'servicios/estado_tramite_form.html', {'form': form})

def estado_tramite_update(request, pk):
    estado_tramite = get_object_or_404(EstadoTramite, pk=pk)
    if request.method == 'POST':
        form = EstadoTramiteForm(request.POST, instance=estado_tramite)
        if form.is_valid():
            form.save()
            return redirect('estado_tramite_list')
    else:
        form = EstadoTramiteForm(instance=estado_tramite)
    return render(request, 'servicios/estado_tramite_form.html', {'form': form, 'estado_tramite': estado_tramite})

def estado_tramite_delete(request, pk):
    estado_tramite = get_object_or_404(EstadoTramite, pk=pk)
    if request.method == 'POST':
        estado_tramite.delete()
        return redirect('estado_tramite_list')
    return render(request, 'servicios/estado_tramite_confirm_delete.html', {'estado': estado_tramite})

def proveedor_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    proveedores = Proveedor.objects.all()

    if query:
        proveedores = proveedores.filter(
            Q(nombre__icontains=query)
        )

    if direction == 'desc':
        order_by = f'-{order_by}'
    proveedores = proveedores.order_by(order_by)

    paginator = Paginator(proveedores, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/proveedor_list.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'servicios/proveedor_form.html', {'form': form})

def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'servicios/proveedor_form.html', {'form': form, 'proveedor': proveedor})

def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'servicios/proveedor_confirm_delete.html', {'proveedor': proveedor})

def nombreservicio_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    nombreservicios = NombreServicio.objects.all()

    if query:
        nombreservicios = nombreservicios.filter(
            Q(nombre__icontains=query)
        )

    if direction == 'desc':
        order_by = f'-{order_by}'
    nombreservicios = nombreservicios.order_by(order_by)

    paginator = Paginator(nombreservicios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/nombreservicio_list.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

def nombreservicio_create(request):
    if request.method == 'POST':
        form = NombreServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nombreservicio_list')
    else:
        form = NombreServicioForm()
    return render(request, 'servicios/nombreservicio_form.html', {'form': form})

def nombreservicio_update(request, pk):
    nombreservicio = get_object_or_404(NombreServicio, pk=pk)
    if request.method == 'POST':
        form = NombreServicioForm(request.POST, instance=nombreservicio)
        if form.is_valid():
            form.save()
            return redirect('nombreservicio_list')
    else:
        form = NombreServicioForm(instance=nombreservicio)
    return render(request, 'servicios/nombreservicio_form.html', {'form': form, 'nombreservicio': nombreservicio})

def nombreservicio_delete(request, pk):
    nombreservicio = get_object_or_404(NombreServicio, pk=pk)
    if request.method == 'POST':
        nombreservicio.delete()
        return redirect('nombreservicio_list')
    return render(request, 'servicios/nombreservicio_confirm_delete.html', {'nombreservicio': nombreservicio})

def contratacion_list(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_finalizacion = request.GET.get('fecha_finalizacion')
    contrataciones = Contratacion.objects.all()
    today = date.today()

    if query:
        contrataciones = contrataciones.filter(
            Q(nombre__nombre__icontains=query) |
            Q(nro_ultima_orden_compra__icontains=query) |
            Q(duracion_meses__icontains=query) |
            Q(fecha_inicio__icontains=query) |
            Q(fecha_finalizacion__icontains=query) |
            Q(saldo_dias__icontains=query) |
            Q(nro_expediente_contratacion__icontains=query) |
            Q(vigente__icontains=query) |
            Q(en_tramite__icontains=query) |
            Q(estado__nombre__icontains=query) |
            Q(sector__nombre__icontains=query)
        )

    if fecha_inicio:
        contrataciones = contrataciones.filter(fecha_inicio__gte=fecha_inicio)
    if fecha_finalizacion:
        contrataciones = contrataciones.filter(fecha_finalizacion__lte=fecha_finalizacion)

    if direction == 'desc':
        order_by = f'-{order_by}'
    contrataciones = contrataciones.order_by(order_by)

    paginator = Paginator(contrataciones, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for contratacion in page_obj:
        contratacion.saldo_dias = (contratacion.fecha_finalizacion - today).days
        contratacion.near_expiration = contratacion.is_near_expiration()

    return render(request, 'servicios/contratacion_list.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction,
        'fecha_inicio': fecha_inicio,
        'fecha_finalizacion': fecha_finalizacion,
        'today': today  # Add this line
    })

def contratacion_create(request):
    today = date.today()
    if request.method == 'POST':
        form = ContratacionForm(request.POST)
        if form.is_valid():
            contratacion = form.save(commit=False)
            contratacion.saldo_dias = (contratacion.fecha_finalizacion - today).days
            contratacion.save()
            return redirect('contratacion_list')
    else:
        form = ContratacionForm()
    return render(request, 'servicios/contratacion_form.html', {'form': form})

def contratacion_update(request, pk):
    contratacion = get_object_or_404(Contratacion, pk=pk)
    if request.method == 'POST':
        form = ContratacionForm(request.POST, instance=contratacion)
        if form.is_valid():
            contratacion = form.save(commit=False)
            contratacion.saldo_dias = (contratacion.fecha_finalizacion - date.today()).days
            contratacion.save()
            return redirect('contratacion_list')
    else:
        form = ContratacionForm(instance=contratacion)
        # Esto asegura que las fechas iniciales se pasen correctamente al formulario
        if contratacion.fecha_inicio:
            form.fields['fecha_inicio'].initial = contratacion.fecha_inicio.strftime('%Y-%m-%d')
        if contratacion.fecha_finalizacion:
            form.fields['fecha_finalizacion'].initial = contratacion.fecha_finalizacion.strftime('%Y-%m-%d')
    return render(request, 'servicios/contratacion_form.html', {'form': form, 'contratacion': contratacion})



def contratacion_delete(request, pk):
    contratacion = get_object_or_404(Contratacion, pk=pk)
    if request.method == 'POST':
        contratacion.delete()
        return redirect('contratacion_list')
    return render(request, 'servicios/contratacion_confirm_delete.html', {'contratacion': contratacion})

def estado_contratacion_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    estados = EstadoContratacion.objects.all()

    if query:
        estados = estados.filter(
            Q(nombre__icontains=query)
        )

    if direction == 'desc':
        order_by = f'-{order_by}'
    estados = estados.order_by(order_by)

    paginator = Paginator(estados, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/estado_contratacion_list.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction,
        'estados': estados  # Asegúrate de pasar 'estados' al contexto
    })

def estado_contratacion_create(request):
    if request.method == 'POST':
        form = EstadoContratacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estado_contratacion_list')
    else:
        form = EstadoContratacionForm()
    return render(request, 'servicios/estado_contratacion_form.html', {'form': form})

def estado_contratacion_update(request, pk):
    estado_contratacion = get_object_or_404(EstadoContratacion, pk=pk)
    if request.method == 'POST':
        form = EstadoContratacionForm(request.POST, instance=estado_contratacion)
        if form.is_valid():
            form.save()
            return redirect('estado_contratacion_list')
    else:
        form = EstadoContratacionForm(instance=estado_contratacion)
    return render(request, 'servicios/estado_contratacion_form.html', {'form': form, 'estado_contratacion': estado_contratacion})

def estado_contratacion_delete(request, pk):
    estado_contratacion = get_object_or_404(EstadoContratacion, pk=pk)
    if request.method == 'POST':
        estado_contratacion.delete()
        return redirect('estado_contratacion_list')
    return render(request, 'servicios/estado_contratacion_confirm_delete.html', {'estado_contratacion': estado_contratacion})

def sector_contratacion_list(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    sectores = SectorContratacion.objects.all()

    if query:
        sectores = sectores.filter(
            Q(nombre__icontains=query)
        )

    if direction == 'desc':
        order_by = f'-{order_by}'
    sectores = sectores.order_by(order_by)

    paginator = Paginator(sectores, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/sector_contratacion_list.html', {'page_obj': page_obj, 'query': query, 'order_by': order_by, 'direction': direction})

def sector_contratacion_create(request):
    if request.method == 'POST':
        form = SectorContratacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sector_contratacion_list')
    else:
        form = SectorContratacionForm()
    return render(request, 'servicios/sector_contratacion_form.html', {'form': form})

def sector_contratacion_update(request, pk):
    sector_contratacion = get_object_or_404(SectorContratacion, pk=pk)
    if request.method == 'POST':
        form = SectorContratacionForm(request.POST, instance=sector_contratacion)
        if form.is_valid():
            form.save()
            return redirect('sector_contratacion_list')
    else:
        form = SectorContratacionForm(instance=sector_contratacion)
    return render(request, 'servicios/sector_contratacion_form.html', {'form': form, 'sector_contratacion': sector_contratacion})

def sector_contratacion_delete(request, pk):
    sector_contratacion = get_object_or_404(SectorContratacion, pk=pk)
    if request.method == 'POST':
        sector_contratacion.delete()
        return redirect('sector_contratacion_list')
    return render(request, 'servicios/sector_contratacion_confirm_delete.html', {'sector_contratacion': sector_contratacion})

def marcar_pagado(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            servicio_id = form.cleaned_data['servicio_id']
            fecha_pago = form.cleaned_data['fecha_pago']
            pagado = form.cleaned_data['pagado']
            servicio = get_object_or_404(Servicio, pk=servicio_id)
            servicio.fecha_pago = fecha_pago
            servicio.pagado = pagado
            try:
                servicio.estado_tramite = EstadoTramite.objects.get(nombre="Pagado")
            except ObjectDoesNotExist:
                pass  # Handle the case where "Pagado" does not exist
            servicio.save()
            return redirect('servicio_list')
    return redirect('servicio_list')

def resumen_servicios(request):
    total_por_ano = Servicio.objects.values('fecha_desde__year').annotate(total=Sum('factura__monto_unitario'))
    total_por_servicio = Servicio.objects.values('nombre__nombre').annotate(total=Sum('factura__monto_unitario'))
    cantidad_por_estado = Servicio.objects.values('estado_tramite__nombre').annotate(cantidad=Count('id'))

    alertas_count = Contratacion.objects.filter(fecha_finalizacion__lte=date.today() + timedelta(days=90)).count()

    context = {
        'total_por_ano': total_por_ano,
        'total_por_servicio': total_por_servicio,
        'cantidad_por_estado': cantidad_por_estado,
        'alertas_count': alertas_count,
    }
    return render(request, 'servicios/resumen_servicios.html', context)

def welcome(request):
    return redirect('resumen_servicios')

def home(request):
    return redirect('resumen_servicios')

def alertas_list(request):
    contrataciones = Contratacion.objects.filter(fecha_finalizacion__lte=date.today() + timedelta(days=90))
    alertas_count = contrataciones.count()
    return render(request, 'servicios/alertas_list.html', {'contrataciones': contrataciones, 'alertas_count': alertas_count})
