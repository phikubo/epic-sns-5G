from django import forms
from .static.simulador.utilidades import config as cfg
#auxiliares
import os
from itertools import zip_longest

#https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html

#------------------------------SIMAPP

#seleccion
geometria_choices=(
        ('autoajustable', 'Radio proporcional a la ISD'),
        ('manual', 'Radio Definido por Usuario'),  
    )

distribucion_choices=(
        ('ppp', 'Proceso Puntual Poisson'),
        #('rand', 'Aleatorio'),
        #('fijo', 'Fijo'),
    )

#indica porcentaje de area
'''
densidad_choices=(
        (0.000002, 'Baja'),
        (0.000005, 'Media'),
        (0.000009, 'Moderada'),
        (0.00009, 'Alta [!]'),
        (0.00001, 'Masivo [!!]'),
        (0.0009, 'Ultra [!!!]'),
    )'''

densidad_choices=(
        (1, 'Baja'),
        (10, 'Media'),
        (100, 'Moderada'),
        (1000, 'Alta [!]'),
        (2000, 'Masivo [!!]'),
        (3000, 'Ultra [!!!]'),
    )

imagen_choices=(
        (True, 'Activado'),
        #(False, 'Desactivado'),
        #funciona solo para presimulacion.
        #si se desea generar por cada toma, es necesario desactivar las banderas
        #correspondientes al archivo de configuracion y el modulo simulador,
        #y el modulo sistema, y adicionmente generar un script que permita
        #almacenar cada toma con un nombre diferente.
    )

#---------------------------------
modelo_perdidas_choices=(
        ('okumura_hata', 'Modelo Okumura Hata'),
        ('uma_3gpp', 'Modelo 3GPP UMa'),
        ('uma_3gpp_opcional','Modelo 3GPP UMa Opc'),
        ('umi_ci', 'Modelo CI-UMi'),
        ('umi_abg', 'Modelo ABG-UMi'),
        
    )

desvancimiento_choices=(
        (False, 'Desactivado'), #NA
        ('normal', 'Normal'), #lento
        ('rayl', 'Rayleight'), #rapido
        ('mixto', 'Normal+Rayleight'), #mixto
        
    )

#----------------------------------------------
antena_choices=(
        ('4g', '38901 Trisectorizada'),
        ('5g', 'Mimo Masivo'),
        #('futuro', 'Futuro**'), 
    )


asignacion_choices=(
        ('rr_hard', 'Round Robin Hard'),
        ('rr_soft', 'Round Robin Soft'),
        #('genetico', 'Genético'),
        #('quantico-g', 'Quántico Genético [no disponible sin un computador cuántico]'),
        #('futuro', 'Futuro*') 
    )

bw_choices=(
        (50, '50 FR1: 270 Rbs'),
        (100, '100 FR1: 273 Rbs'),
        (200, '200 FR2: 264 Rbs'),
        (400, '400 FR2: 264 Rbs'), 
  
    )

#----------------------------------------------
#end

class FormComparacion(forms.Form):
    '''De una lista de escenarios, configura los parametros de resultados disponibles'''
    contenido = os.listdir('simapp/static/simulador/base_datos/imagenes/resultados')
    contenido.remove('leeme')
    contenido_rutas=["simapp/static/simulador/base_datos/imagenes/resultados/"+i for i in contenido]
    escenario_choices = dict(zip_longest(contenido_rutas, contenido))
    escenario_choices=tuple(escenario_choices.items())
    escenario_opcion_1=forms.ChoiceField(label='Escenario 1 a comparar:',choices=escenario_choices)
    escenario_opcion_2=forms.ChoiceField(label='Escenario 2 a comparar:',choices=escenario_choices)


class FormSeleccion(forms.Form):
    '''De una lista de escenarios, configura la variable escenario activo que es el archivo de configuración que se simula'''
    escenario_choices=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
    #escenario_choices=(tuple(escenario_choices["rutas_configuracion"].items()))
    #print("opciones\n",escenario_choices)
    reversed_dict = dict(map(reversed, escenario_choices["rutas_configuracion"].items()))
    escenario_choices=tuple(reversed_dict.items())
    escenario_opciones=forms.ChoiceField(label='Escenarios Disponibles',choices=escenario_choices)

class FormCompacto(forms.Form):
    '''Formulario inicial. Configura parametros globales'''
    nombre_archivo=forms.CharField(label='Nombre del Escenario',max_length=100)
    iteraciones=forms.IntegerField(label='Realizaciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [MHz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia entre Celdas [m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Tipo de distribución de MS',choices=geometria_choices)
    radio_cel=forms.IntegerField(label='Radio de la Celda [m]', initial=1000, min_value=5)
    tipo_distribucion=forms.ChoiceField(label='Distribución de MS',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de MS',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=50, max_value=1000, min_value=10)

    '''Formulario para configurar variables relacionadas al modelo de perdidas de propagación'''
    modelo_perdidas=forms.ChoiceField(label='Modelo de Pérdidas de Propagación',choices=modelo_perdidas_choices)
    #floats
    mp1=forms.DecimalField(label='Altura Antena',initial=25, min_value=0, max_digits=5, decimal_places=2)
    mp2=forms.DecimalField(label='Parámero 2',initial=0, min_value=0, max_digits=5, decimal_places=2, disabled=True)
    mp3=forms.DecimalField(label='Altura Terminal',initial=1.5, min_value=0, max_digits=5, decimal_places=2)
    mp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2, disabled=True)

    params_desv=forms.ChoiceField(label='Tipo de Desvanecimiento',choices=desvancimiento_choices)
    #flats
    dp1=forms.DecimalField(label='Parámero 1',initial=3.1, min_value=0, max_digits=5, decimal_places=2)
    dp2=forms.DecimalField(label='Parámero 2',initial=8.1, min_value=0, max_digits=5, decimal_places=2)
    dp3=forms.DecimalField(label='Parámero 3',initial=0, min_value=0, max_digits=5, decimal_places=2, disabled=True)
    dp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2, disabled=True)

    ber_sinr=forms.DecimalField(label='SINR Objetivo [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    nf=forms.DecimalField(label='Figura de Ruido en el Receptor [dB]',initial=6, min_value=1, max_digits=5, decimal_places=2)

    '''Formulario para configurar variables relacionadas al balance del enlace y las antenas'''
    ptx=forms.DecimalField(label='Potencia de Transmisión [dBm]',initial=28, min_value=1, max_digits=5, decimal_places=2)
    gtx=forms.DecimalField(label='Ganancia Máxima de Antena en Transmisión [dBi]',initial=15, min_value=1, max_digits=5, decimal_places=2)
    ltx=forms.DecimalField(label='Pérdidas en Transmisión [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    lrx=forms.DecimalField(label='Pérdidas en Recepción [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    grx=forms.DecimalField(label='Ganancia Máxima de Antena en Recepción [dBi]',initial=8, min_value=1, max_digits=5, decimal_places=2)
    #sensibilidad=forms.DecimalField(label='Sensibilidad en Recepción [dBm]',initial=-98, max_digits=5, decimal_places=2)
    mcl=forms.DecimalField(label='MCL [dB]',initial=70, min_value=1, max_digits=5, decimal_places=2)
    #antenas
    tipo_antena=forms.ChoiceField(label='Tipo Antena',choices=antena_choices)
    hpbw=forms.IntegerField(label='Ancho de Haz [°]',initial=65, min_value=1)
    apuntamiento=forms.IntegerField(label='Dirección de Máxima Radiación [°]',initial=30, min_value=1)
    atmin=forms.DecimalField(label='Atenuación Mínima [dB]',initial=20, min_value=1, max_digits=5, decimal_places=2)
    
    '''Formulario para configurar variables relacionadas a la asignación de recursos radio.'''
    tipo_asignacion=forms.ChoiceField(label='Tipo de Asignación',choices=asignacion_choices)
    #bw=forms.IntegerField(label='Ancho de Banda Usuario [MHz]',initial=20, min_value=10)
    bw=forms.ChoiceField(label='Ancho de Banda del Sistema [MHz]',choices=bw_choices, help_text="Frecuencia < 6GHz: FR1. Frecuencia > 6GHz: FR2.")
    #numerologia=forms.IntegerField(label='Numerología Default',initial=0, min_value=1, disabled=True)
    #banda_guarda=forms.IntegerField(label='Banda de Guarda [KHz]',initial=845, min_value=1, disabled=True, widget=forms.HiddenInput())
    subportadora=forms.IntegerField(label='Número de Subportadoras (frecuencia)',initial=12, min_value=1, disabled=True)
    trama=forms.IntegerField(label='Número Total de Símbolos OFDM (tiempo)',initial=14,min_value=1, disabled=True)
    simbolos=forms.IntegerField(label='Número de Símbolos OFDM',initial=12, min_value=1, disabled=True)
    frame=forms.IntegerField(label='Número de Subtrama',initial=10, min_value=1, disabled=True)
    #
    futuro1=forms.IntegerField(label='Futuro*',initial=0, min_value=0, disabled=True)
    futuro2=forms.IntegerField(label='Futuro**',initial=0, min_value=0, disabled=True)
    
    