from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
#lista de formularios
from .forms import FormStepOne, FormStepTwo
#
# Create your views here.
def home(request):
    return render(request,'simapp/sami-index.html')

def form_demo_sami_v1(request):
    return render(request,'simapp/sami-demo-v1.html')

def en_desarrollo(request):
    return render(request,'simapp/sami-en-desarrollo.html')

def test_sam(request):
    return render(request,'simapp/sami-formulario-v1.html')


class FormWizardView(SessionWizardView):
    template_name = "simapp/sami-formulario-v1.html"
    form_list = [FormStepOne, FormStepTwo]
    def done(self, form_list, **kwargs):
        #
        for form in form_list:
            print(form.cleaned_data)

        return render(self.request, 'simapp/sami-en-desarrollo.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
    
#guardar cada lista de variables 
#lo anterior por cada pagina
#al subir la informacion final, 
#generar una nueva pagina endpoint donde esta el boton simular
 #https://www.youtube.com/watch?v=DzGwrSh1S50&feature=emb_title
 #https://django-formtools.readthedocs.io/en/latest/wizard.html#how-it-works
 #https://www.youtube.com/watch?v=zNbyQY00DI8
 #this first https://www.youtube.com/watch?v=90M4gunBRLs
 #base https://swapps.com/blog/how-to-do-a-wizard-form/
 #base video https://www.youtube.com/watch?v=fSnBF-BmccQ
 #http://127.0.0.1:8000/test/
 #get template https://supercoders.in/python-django-multi-step-form-example/  