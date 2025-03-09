import datetime
from django import forms
from django.forms import inlineformset_factory
from .models import Servicio, Factura, Contratacion, TipoTramite, EstadoTramite, Proveedor, NombreServicio, EstadoContratacion, SectorContratacion

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'fecha_desde': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'required': 'required'}),
            'fecha_hasta': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'required': 'required'}),
            'vencimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_inicio_tramite': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_pago': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].queryset = NombreServicio.objects.all()
        self.fields['tipo_tramite'].queryset = TipoTramite.objects.all()
        self.fields['estado_tramite'].queryset = EstadoTramite.objects.all()
        self.fields['proveedor'].queryset = Proveedor.objects.all()

        # Convertir fechas al formato correcto si hay valores iniciales
        for field_name in ['fecha_desde', 'fecha_hasta', 'vencimiento', 'fecha_inicio_tramite', 'fecha_pago']:
            if self.instance.pk and getattr(self.instance, field_name):
                fecha = getattr(self.instance, field_name)
                self.fields[field_name].initial = fecha.strftime('%Y-%m-%d')  # Formato correcto para HTML

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['nro_factura', 'monto_unitario']

FacturaFormSet = inlineformset_factory(Servicio, Factura, form=FacturaForm, extra=1, can_delete=True)

class ContratacionForm(forms.ModelForm):
    class Meta:
        model = Contratacion
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_finalizacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].queryset = NombreServicio.objects.all()  # Asegurarse de que el queryset esté disponible

        # Convertir fechas al formato correcto si hay valores iniciales
        for field_name in ['fecha_inicio', 'fecha_finalizacion']:
            if self.instance.pk and getattr(self.instance, field_name):
                fecha = getattr(self.instance, field_name)
                self.fields[field_name].initial = fecha.strftime('%Y-%m-%d')  # Formato correcto para HTML



class TipoTramiteForm(forms.ModelForm):
    class Meta:
        model = TipoTramite
        fields = '__all__'

class EstadoTramiteForm(forms.ModelForm):
    class Meta:
        model = EstadoTramite
        fields = '__all__'

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class NombreServicioForm(forms.ModelForm):
    class Meta:
        model = NombreServicio
        fields = '__all__'

class EstadoContratacionForm(forms.ModelForm):
    class Meta:
        model = EstadoContratacion
        fields = '__all__'

class SectorContratacionForm(forms.ModelForm):
    class Meta:
        model = SectorContratacion
        fields = '__all__'

class PagoForm(forms.Form):
    servicio_id = forms.IntegerField(widget=forms.HiddenInput())
    fecha_pago = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    pagado = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
