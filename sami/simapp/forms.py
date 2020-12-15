from django import forms
#https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
class FormStepOne(forms.Form):
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1)
    nombre= forms.CharField(max_length=100,initial="name")
    Apellido = forms.CharField(max_length=100,initial="last")
    Telefono  = forms.CharField(max_length=100,initial="number")

class FormStepTwo(forms.Form):
    job = forms.CharField(max_length=100,initial="name")
    salary = forms.CharField(max_length=100,initial="name")
    job_description = forms.CharField(widget=forms.Textarea,initial="name")

#------------------------------SIMAPP
class FormGeneral(forms.Form):
    iteraciones=forms.IntegerField(label='Iteraciones',initial=1)
    n_celdas=forms.IntegerField(initial=1)
    #geometria_usuarios=forms.IntegerField()
    radio_cel=forms.IntegerField(initial=1000)
    #distribucion= #choice
    #portadora=#choice 
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