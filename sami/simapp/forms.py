from django import forms
#from .simulador_v1.utilidades import config as cfg
#https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
class FormStepOne(forms.Form):
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1)
    nombre= forms.CharField(max_length=100,initial="name")
    Apellido = forms.CharField(max_length=100,initial="last")
    Telefono  = forms.CharField(max_length=100,initial="number")
    otro  = forms.CharField(max_length=100,initial="number")
    otro2  = forms.CharField(max_length=100,initial="number")
    otro3  = forms.CharField(max_length=100,initial="number")
    otro4  = forms.CharField(max_length=100,initial="number")
    otro5  = forms.CharField(max_length=100,initial="number")

class FormStepTwo(forms.Form):
    job = forms.CharField(max_length=100,initial="name")
    salary = forms.CharField(max_length=100,initial="name")
    job_description = forms.CharField(widget=forms.Textarea,initial="name")

#------------------------------SIMAPP
#seleccion
geometria_choices=(
        ('autoajustable', 'Radio proporcional a ISD'),
        ('manual', 'Radio Customizado'),  
    )

distribucion_choices=(
        ('ppp', 'Proceso Puntual Poissson'),
        ('rand', 'Aleatorio'),
        ('fijo', 'Fijo'),
    )

densidad_choices=(
        (0.000002, 'Baja'),
        (0.000005, 'Media'),
        (0.000009, 'Moderada'),
        (0.00009, 'Alta [!]'),
        (0.00001, 'Masivo [!!]'),
        (0.0009, 'Ultra [!!!]'),
    )

imagen_choices=(
        (False, 'Desactivado'),
        (True, 'Activado'),

    )

#---------------------------------
modelo_perdidas_choices=(
        ('okumura_hata', 'Modelo Okumura Hata'),
        ('uma_3gpp', 'Modelo 3GPP UMa'),
        ('umi_ci', 'Modelo CI-UMi'),
        ('umi_abg', 'Modelo ABG-UMi'),
        
    )

desvancimiento_choices=(
        ('desactivado', 'Desactivado'),
        ('normal', 'Normal'),
        ('rayl', 'Rayleight'),
        ('mixto', 'Normal+Rayleight'),
        
    )
#end
class FormGeneral(forms.Form):
    '''Formulario inicial. Configura parametros globales'''
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [Mhz, Ghz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia Entre Celdas [m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(initial=1000, min_value=10)
    tipo_distribucion=forms.ChoiceField(label='Tipo de Despliegue de Usuarios',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de Población',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=1000, max_value=2000, min_value=10) 



class FormPropagacion(forms.Form):
    '''Formulario para configurar variables relacionadas al modelo de perdidas de propagación'''
    modelo_perdidas=forms.ChoiceField(label='Modelo de Pérdidas de Propagación',choices=modelo_perdidas_choices)
    #floats
    mp1=forms.DecimalField(label='Parámero 1',initial=1, min_value=1, max_digits=5, decimal_places=2)
    mp2=forms.DecimalField(label='Parámero 2',initial=1, min_value=1, max_digits=5, decimal_places=2)
    mp3=forms.DecimalField(label='Parámero 3',initial=1, min_value=1, max_digits=5, decimal_places=2)
    mp4=forms.DecimalField(label='Parámero 4',initial=1, min_value=1, max_digits=5, decimal_places=2)

    params_desv=forms.ChoiceField(label='Tipo de Desvanecimiento',choices=desvancimiento_choices)
    #flats
    dp1=forms.DecimalField(label='Parámero 1',initial=1, min_value=1, max_digits=5, decimal_places=2)
    dp2=forms.DecimalField(label='Parámero 2',initial=1, min_value=1, max_digits=5, decimal_places=2)
    dp3=forms.DecimalField(label='Parámero 3',initial=1, min_value=1, max_digits=5, decimal_places=2)
    dp4=forms.DecimalField(label='Parámero 4',initial=1, min_value=1, max_digits=5, decimal_places=2)

    ber_sinr=forms.DecimalField(label='BER Objetivo [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    nf=forms.DecimalField(label='Figura de Ruido [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)


class FormBalance(forms.Form):
    '''Formulario para configurar variables relacionadas al balance del enlace y las antenas'''
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [Mhz, Ghz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia Entre Celdas [m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(initial=1000, min_value=10)
    tipo_distribucion=forms.ChoiceField(label='Tipo de Despliegue de Usuarios',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de Población',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=1000, max_value=2000, min_value=10) 


class FormAntenas(forms.Form):
    '''Formulario para configurar variables relacionadas a las antenas. Fue Combinado en Balance.'''
    pass

class FormAsignacion(forms.Form):
    '''Formulario para configurar variables relacionadas a la asignación de recursos radio.'''
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [Mhz, Ghz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia Entre Celdas [m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(initial=1000, min_value=10)
    tipo_distribucion=forms.ChoiceField(label='Tipo de Despliegue de Usuarios',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de Población',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=1000, max_value=2000, min_value=10) 
