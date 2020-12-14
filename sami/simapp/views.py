from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
#lista de formularios
from .forms import FormStepOne, FormStepTwo
#
# Create your views here.
def home(request):
    return render(request,'simapp/sami-index.html')

def formulario_sami_v1(request):
    return render(request,'simapp/form-wizard.html')

def en_desarrollo(request):
    return render(request,'simapp/sami-en-desarrollo.html')

def test_sam(request):
    return render(request,'simapp/sami-formulario-v1.html')


class FormWizardView(SessionWizardView):
    template_name = "simapp/sami-formulario-v1.html"
    form_list = [FormStepOne, FormStepTwo]
    def done(self, form_list, **kwargs):
        for form in form_list:
            print(form.cleaned_data)
        return render(self.request, 'simapp/sami-en-desarrollo.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
    
#guardar cada lista de variables 
#lo anterior por cada pagina
#al subir la informacion final, 
#generar una nueva pagina endpoint donde esta el boton simular
   