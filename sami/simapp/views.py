from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
#form tools
from formtools.wizard.views import SessionWizardView
#lista de formularios
from .forms import FormStepOne, FormStepTwo
from .forms import FormGeneral, FormPropagacion
#integracion simulador
import os
import json
from .simulador_v1.utilidades import config as cfg
from .simulador_v1 import top_pruebas 
#configuracion=cfg.cargar_variables(target_path="simulador_v1/base_datos/")

#test_integracion
global_test=True
def convertir_str_2_bool(check):
    '''Convierte "True" o "False" a True o False'''
    res=False
    if check=="True":
        res=True
    else:
        pass

    return res


# Create your views here.
def home(request):
    return render(request,'simapp/sami-index.html')

def form_demo_sami_v1(request):
    return render(request,'simapp/sami-demo-v1.html')
#os.path.realpath('./modules')

def en_desarrollo(request):
    return render(request,'simapp/sami-en-desarrollo.html')

def iniciar_simulacion(request):
    if request.method == 'GET':
        try:
            arr = os.listdir()
            print(arr)
            

        except Exception as ex:
            print(ex)
        #exists = os.path.isfile('/path/to/file')
        #print(exists)
        print("GET Metodo")
        top_pruebas.prueba_sistema_v048()
    return render(request,'simapp/sami-iniciar-sim.html')

def ver_estadisticas(request):
    return render(request,'simapp/sami-sim-estadisticas.html')
#def test_sam(request):
    return render(request,'simapp/sami-form-test1.html')


#FORMULARIOS V1
def form_a1(request):
    form=FormGeneral()
    if request.method == 'POST':
        form=FormGeneral(request.POST)
        print("\nHA OCURRIDO UN POST")
        if form.is_valid():
            #CONFIGURACION DE VARIABLES
            print("[OK]-Formulario 1 Aceptado")
            contenido=form.cleaned_data

            config=cfg.cargar_variables(target_path="simapp/simulador_v1/base_datos/")
            config["cfg_simulador"]["params_general"]["iteracion"]=contenido["iteraciones"]
            config["cfg_simulador"]["params_general"]["n_celdas"]=contenido["n_celdas"]
            config["cfg_simulador"]["params_general"]["portadora"][0]=contenido["portadora"]
            config["cfg_simulador"]["params_general"]["isd"]=contenido["isd"]
            
            config["cfg_simulador"]["params_general"]["geometria"]=contenido["geometria_usuarios"]
            config["cfg_simulador"]["params_general"]["radio_cel"]=contenido["radio_cel"] 

            config["cfg_simulador"]["params_general"]["distribucion"][0]=contenido["tipo_distribucion"]
            config["cfg_simulador"]["params_general"]["distribucion"][1]=float(contenido["densidad"])
                        
            flag_imagen=convertir_str_2_bool(contenido["imagen"])
            config["cfg_simulador"]["params_general"]["imagen"]["display"][0]=flag_imagen
            config["cfg_simulador"]["params_general"]["imagen"]["resolucion"]=contenido["pixeles"]
            cfg.guardar_cfg2(config, target_path="simapp/simulador_v1/base_datos/")
        else:
            print("Oops, algo ha fallado. Retornando.")
            return redirect('/sim/')
        #no necesario con validators
        #if int(request.POST["isd"])>1200:
        #    return redirect('/sim')
        #-----------
        #SIGUIENTE
        return redirect('/sim/form_a2')
    #-----------
    #ACTUAL
    return render(request,'simapp/form_v1/sami-form-a1.html', {"form_data":form} )


def form_a2(request):
    form=FormPropagacion()
    if request.method == 'POST':
        form=FormPropagacion(request.POST)
        print("\nHA OCURRIDO UN POST a2 \n",request.POST)
        if form.is_valid():
            #CONFIGURACION DE VARIABLES
            print("[OK]-Formulario a2 Aceptado")
            contenido=form.cleaned_data
            print(contenido)
            '''
            config=cfg.cargar_variables(target_path="simapp/simulador_v1/base_datos/")
            config["cfg_simulador"]["params_general"]["iteracion"]=contenido["iteraciones"]
            config["cfg_simulador"]["params_general"]["n_celdas"]=contenido["n_celdas"]
            config["cfg_simulador"]["params_general"]["portadora"][0]=contenido["portadora"]
            config["cfg_simulador"]["params_general"]["isd"]=contenido["isd"]
            
            config["cfg_simulador"]["params_general"]["geometria"]=contenido["geometria_usuarios"]
            config["cfg_simulador"]["params_general"]["radio_cel"]=contenido["radio_cel"] 

            config["cfg_simulador"]["params_general"]["distribucion"][0]=contenido["tipo_distribucion"]
            config["cfg_simulador"]["params_general"]["distribucion"][1]=float(contenido["densidad"])
                        
            flag_imagen=convertir_str_2_bool(contenido["imagen"])
            config["cfg_simulador"]["params_general"]["imagen"]["display"][0]=flag_imagen
            config["cfg_simulador"]["params_general"]["imagen"]["resolucion"]=contenido["pixeles"]
            '''
        #-----------
        #SIGUIENTE
        #return render(request,'simapp/form_v1/sami-form-a3.html')
        return redirect('/sim/form_a3')
    #-----------
    #ACTUAL
    return render(request,'simapp/form_v1/sami-form-a2.html', {"form_data":form} )


def form_a3(request):
    form=FormGeneral()
    if request.method == 'POST':
        form=FormGeneral(request.POST)
        print("\nHA OCURRIDO UN POST a3", request.POST)
        #iteracion= form.cleaned_data['iteraciones']
        #celdas = form.cleaned_data['n_celdas']
        #-----------
        #SIGUIENTE
        #return render(request,'simapp/form_v1/sami-form-a4.html')
        return redirect('/sim/form_a4')
    #-----------
    #ACTUAL
    else:
        print("HA OCURRIDO OTRA COSA a3")
    return render(request,'simapp/form_v1/sami-form-a3.html', {"form_data":form} )


def form_a4(request):
    form=FormGeneral()
    if request.method == 'POST':
        form=FormGeneral(request.POST)
        print("\nHA OCURRIDO UN POST a4", request.POST)
        #iteracion= form.cleaned_data['iteraciones']
        #celdas = form.cleaned_data['n_celdas']
        #-----------
        #SIGUIENTE
        return redirect('iniciar/')
    #-----------
    #ACTUAL
    else:
        print("HA OCURRIDO OTRA COSA a4")
    return render(request,'simapp/form_v1/sami-form-a4.html', {"form_data":form} )





#AUXILIAR Y PRUEBAS

class FormWizardView(SessionWizardView):
    template_name = "simapp/sami-form-test1.html"
    form_list = [FormStepOne, FormStepTwo]
    def done(self, form_list, **kwargs):
        #
        for form in form_list:
            print(form.cleaned_data)

        return render(self.request, 'simapp/sami-en-desarrollo.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


def form_view_2(request):
    form=FormGeneral()
    if request.method == 'POST':
        print("POST Metodo")
        #iteracion= form.cleaned_data['iteraciones']
        #celdas = form.cleaned_data['n_celdas']
        print(".post", request.POST)
        return render(request,'simapp/sami-en-desarrollo.html')
    return render(request,'simapp/sami-form-test2.html', {"form_data":form} )

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