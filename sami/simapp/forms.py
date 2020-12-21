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
        ('1', 'Manual'),
        ('2', 'Automático'),
    )

distribucion_choices=(
        ('ppp', 'Proceso Puntual Poissson'),
        ('rand', 'Aleatorio'),
        ('fijo', 'Fijo'),
    )

distribucion_choices=(
        (0.000002, 'Baja'),
        (0.0000015, 'Alta'),
        (0.0000010, 'Media'),
        (0.000001, 'Ultra [!]'),
    )
#end
class FormGeneral(forms.Form):
    #configuracion=cfg.cargar_variables(target_path="simapp/simulador_v1/base_datos/")
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1)
    n_celdas=forms.IntegerField(label='Cantidad de Celdas',initial=1)
    #portadora=forms.IntegerField(label='Frecuencia Portadora [Mhz, Ghz]',initial=900)
    portadora=forms.ChoiceField(label='Geometria de Distribución de Usuarios',choices=geometria_choices)
    isd=forms.IntegerField(label='Distancia Entre Celdas [m]',initial=1000)
    geometria_usuarios=forms.ChoiceField(label='Geometria de Distribución de Usuarios',choices=geometria_choices)
    radio_cel=forms.IntegerField(initial=1000)
    #distribucion= #choice
    distribucion=forms.ChoiceField(label='Geometria de Distribución de Usuarios',choices=geometria_choices)
    #portadora=#choice 
    
    densidad=forms.ChoiceField(label='Geometria de Distribución de Usuarios',choices=geometria_choices)
    nf=forms.IntegerField(initial=6)
    ber_sinr=forms.IntegerField(initial=0)
    imagen=forms.BooleanField(required=False) 



class FormPropagacion(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)

class FormBalance(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)

class FormAntenas(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)

class FormAsignacion(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)