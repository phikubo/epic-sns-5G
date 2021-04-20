from django import forms

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
        ('umi_ci', 'Modelo CI-UMi'),
        ('umi_abg', 'Modelo ABG-UMi'),
        
    )

desvancimiento_choices=(
        (False, 'Desactivado'),
        ('normal', 'Normal'),
        ('rayl', 'Rayleight'),
        ('mixto', 'Normal+Rayleight'),
        
    )

#----------------------------------------------
antena_choices=(
        ('4g', '38942 Trisectorizada'),
        ('5g', 'Futuro*'),
        ('futuro', 'Futuro**'), 
    )


asignacion_choices=(
        ('rr', 'Round Robin'),
        ('f1', 'Futuro*'),
        ('f2', 'Futuro**'), 
    )

bw_choices=(
        (10, '10'),
        (20, '20'),
        (40, '40'),
        (100, '100'), 
        (200, '200'), 
        (400, '400'),  
    )

#----------------------------------------------
#end
class FormGeneral(forms.Form):
    '''Formulario inicial. Configura parametros globales'''
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [MHz, GHz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia entre Celdas (ISD)[m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(label='Radio de la Celda [m]', initial=1000, min_value=5)
    tipo_distribucion=forms.ChoiceField(label='Usuarios por Realización',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de Usuarios',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=50, max_value=1000, min_value=10) 



class FormPropagacion(forms.Form):
    '''Formulario para configurar variables relacionadas al modelo de perdidas de propagación'''
    modelo_perdidas=forms.ChoiceField(label='Modelo de Pérdidas de Propagación',choices=modelo_perdidas_choices)
    #floats
    mp1=forms.DecimalField(label='Parámero 1',initial=30, min_value=0, max_digits=5, decimal_places=2)
    mp2=forms.DecimalField(label='Parámero 2',initial=0, min_value=0, max_digits=5, decimal_places=2)
    mp3=forms.DecimalField(label='Parámero 3',initial=1.5, min_value=0, max_digits=5, decimal_places=2)
    mp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2)

    params_desv=forms.ChoiceField(label='Tipo de Desvanecimiento',choices=desvancimiento_choices)
    #flats
    dp1=forms.DecimalField(label='Parámero 1',initial=3.1, min_value=0, max_digits=5, decimal_places=2)
    dp2=forms.DecimalField(label='Parámero 2',initial=8.1, min_value=0, max_digits=5, decimal_places=2)
    dp3=forms.DecimalField(label='Parámero 3',initial=0, min_value=0, max_digits=5, decimal_places=2)
    dp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2)

    ber_sinr=forms.DecimalField(label='SINR Objetivo [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    nf=forms.DecimalField(label='Figura de Ruido en el Receptor [dB]',initial=6, min_value=1, max_digits=5, decimal_places=2)


class FormBalanceAntenas(forms.Form):
    '''Formulario para configurar variables relacionadas al balance del enlace y las antenas'''
    ptx=forms.DecimalField(label='Potencia de Transmisión [dBm]',initial=28, min_value=1, max_digits=5, decimal_places=2)
    gtx=forms.DecimalField(label='Ganancia Máxima de Antena en Transmisión [dBi]',initial=15, min_value=1, max_digits=5, decimal_places=2)
    ltx=forms.DecimalField(label='Pérdidas en Transmisión [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    lrx=forms.DecimalField(label='Pérdidas en Recepción [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    grx=forms.DecimalField(label='Ganancia Máxima de Antena en Recepción [dBi]',initial=8, min_value=1, max_digits=5, decimal_places=2)
    sensibilidad=forms.DecimalField(label='Sensibilidad en Recepción [dBm]',initial=-98, max_digits=5, decimal_places=2)
    mcl=forms.DecimalField(label='MCL [dB]',initial=70, min_value=1, max_digits=5, decimal_places=2)
    #antenas
    tipo_antena=forms.ChoiceField(label='Tipo Antena',choices=antena_choices)
    hpbw=forms.IntegerField(label='Ancho de Haz [°]',initial=65, min_value=1)
    apuntamiento=forms.IntegerField(label='Dirección de Máxima Radiación [°]',initial=30, min_value=1)
    atmin=forms.DecimalField(label='Atenuación Mínima [dB]',initial=20, min_value=1, max_digits=5, decimal_places=2)
    

class FormAntenas(forms.Form):
    '''Formulario para configurar variables relacionadas a las antenas. Fue Combinado en Balance.'''
    pass

class FormAsignacion(forms.Form):
    '''Formulario para configurar variables relacionadas a la asignación de recursos radio.'''
    tipo_asignacion=forms.ChoiceField(label='Tipo de Asignación',choices=asignacion_choices)
    #bw=forms.IntegerField(label='Ancho de Banda Usuario [MHz]',initial=20, min_value=10)
    bw=forms.ChoiceField(label='Ancho de Banda del Sistema [MHz]',choices=bw_choices)
    numerologia=forms.IntegerField(label='Numerología',initial=1, min_value=1)
    banda_guarda=forms.IntegerField(label='Banda de Guarda [KHz]',initial=845, min_value=1)
    subportadora=forms.IntegerField(label='Número de Subportadoras',initial=12, min_value=1)
    trama=forms.IntegerField(label='Número Total de Intervalos',initial=12,min_value=1)
    simbolos=forms.IntegerField(label='Número de Símbolos OFDM',initial=10, min_value=1)
    frame=forms.IntegerField(label='Número de Símbolos por Trama ',initial=10, min_value=1)
    #
    futuro1=forms.IntegerField(label='Futuro*',initial=0, min_value=0)
    futuro2=forms.IntegerField(label='Futuro**',initial=0, min_value=0)
    
class FormCompacto(forms.Form):
    '''Formulario inicial. Configura parametros globales'''
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1, min_value=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1, max_value=19, min_value=1)
    portadora=forms.IntegerField(label='Frecuencia Portadora [MHz, GHz]',initial=900, min_value=200, max_value=75000,)
    isd=forms.IntegerField(label='Distancia entre Celdas [m]',initial=1000, min_value=10)
    geometria_usuarios=forms.ChoiceField(label='Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(label='Radio de la Celda [m]', initial=1000, min_value=5)
    tipo_distribucion=forms.ChoiceField(label='Usuarios por Realización',choices=distribucion_choices)
    densidad=forms.ChoiceField(label='Densidad de Usuarios',choices=densidad_choices)
    imagen=forms.ChoiceField(required=False,label='Imagen de Potencia Recibida',choices=imagen_choices)
    pixeles=forms.IntegerField(required=False,initial=50, max_value=1000, min_value=10)

    '''Formulario para configurar variables relacionadas al modelo de perdidas de propagación'''
    modelo_perdidas=forms.ChoiceField(label='Modelo de Pérdidas de Propagación',choices=modelo_perdidas_choices)
    #floats
    mp1=forms.DecimalField(label='Parámero 1',initial=30, min_value=0, max_digits=5, decimal_places=2)
    mp2=forms.DecimalField(label='Parámero 2',initial=0, min_value=0, max_digits=5, decimal_places=2)
    mp3=forms.DecimalField(label='Parámero 3',initial=1.5, min_value=0, max_digits=5, decimal_places=2)
    mp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2)

    params_desv=forms.ChoiceField(label='Tipo de Desvanecimiento',choices=desvancimiento_choices)
    #flats
    dp1=forms.DecimalField(label='Parámero 1',initial=3.1, min_value=0, max_digits=5, decimal_places=2)
    dp2=forms.DecimalField(label='Parámero 2',initial=8.1, min_value=0, max_digits=5, decimal_places=2)
    dp3=forms.DecimalField(label='Parámero 3',initial=0, min_value=0, max_digits=5, decimal_places=2)
    dp4=forms.DecimalField(label='Parámero 4',initial=0, min_value=0, max_digits=5, decimal_places=2)

    ber_sinr=forms.DecimalField(label='SINR Objetivo [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    nf=forms.DecimalField(label='Figura de Ruido en el Receptor [dB]',initial=6, min_value=1, max_digits=5, decimal_places=2)

    '''Formulario para configurar variables relacionadas al balance del enlace y las antenas'''
    ptx=forms.DecimalField(label='Potencia de Transmisión [dBm]',initial=28, min_value=1, max_digits=5, decimal_places=2)
    gtx=forms.DecimalField(label='Ganancia Máxima de Antena en Transmisión [dBi]',initial=15, min_value=1, max_digits=5, decimal_places=2)
    ltx=forms.DecimalField(label='Pérdidas en Transmisión [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    lrx=forms.DecimalField(label='Pérdidas en Recepción [dB]',initial=1, min_value=1, max_digits=5, decimal_places=2)
    grx=forms.DecimalField(label='Ganancia Máxima de Antena en Recepción [dBi]',initial=8, min_value=1, max_digits=5, decimal_places=2)
    sensibilidad=forms.DecimalField(label='Sensibilidad en Recepción [dBm]',initial=-98, max_digits=5, decimal_places=2)
    mcl=forms.DecimalField(label='MCL [dB]',initial=70, min_value=1, max_digits=5, decimal_places=2)
    #antenas
    tipo_antena=forms.ChoiceField(label='Tipo Antena',choices=antena_choices)
    hpbw=forms.IntegerField(label='Ancho de Haz [°]',initial=65, min_value=1)
    apuntamiento=forms.IntegerField(label='Dirección de Máxima Radiación [°]',initial=30, min_value=1)
    atmin=forms.DecimalField(label='Atenuación Mínima [dB]',initial=20, min_value=1, max_digits=5, decimal_places=2)
    
    '''Formulario para configurar variables relacionadas a la asignación de recursos radio.'''
    tipo_asignacion=forms.ChoiceField(label='Tipo de Asignación',choices=asignacion_choices)
    #bw=forms.IntegerField(label='Ancho de Banda Usuario [MHz]',initial=20, min_value=10)
    bw=forms.ChoiceField(label='Ancho de Banda del Sistema [MHz]',choices=bw_choices)
    numerologia=forms.IntegerField(label='Numerología',initial=1, min_value=1, disabled=True)
    banda_guarda=forms.IntegerField(label='Banda de Guarda [KHz]',initial=845, min_value=1)
    subportadora=forms.IntegerField(label='Número de Subportadoras',initial=12, min_value=1, disabled=True)
    trama=forms.IntegerField(label='Número Total de Intervalos',initial=12,min_value=1, disabled=True)
    simbolos=forms.IntegerField(label='Número de Símbolos OFDM',initial=10, min_value=1, disabled=True)
    frame=forms.IntegerField(label='Número de Símbolos por Trama ',initial=10, min_value=1, disabled=True)
    #
    futuro1=forms.IntegerField(label='Futuro*',initial=0, min_value=0)
    futuro2=forms.IntegerField(label='Futuro**',initial=0, min_value=0)
    
    