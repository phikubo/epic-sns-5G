from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
#form tools
from formtools.wizard.views import SessionWizardView
#
#
#fomularios simulador
from .forms import *
#from .forms import FormGeneral, FormPropagacion, FormBalanceAntenas,FormAsignacion
from .forms import FormSeleccion
from .forms import FormCompacto
from .forms import FormComparacion
#integracion simulador
import os
import json
#
import pyfiglet
#
#from .static.simulador import top_pruebas
print("From django.views:")
from .static.simulador import MAIN_simulador as samiv1
from .static.simulador.utilidades import config as cfg


#--------------------------------------
#--------------------------------------
'''Definiciones Globales'''
#--------------------------------------
#--------------------------------------

#--------------------------------------
#--------------------------------------
'''Definiciones Auxiliares'''
#--------------------------------------
#--------------------------------------
def convertir_str_2_bool(check):
    '''Convierte "True" o "False" a True o False'''
    res=False
    if check=="True":
        res=True
    else:
        pass
    return res


def validar_desvanecimiento(check):
    '''Valida el contenido de la variable desvanecimiento y ajusta los parametros'''
    flag=True
    if check=="False":
        flag=False
        tipo="none"
    else:
        flag=True
        tipo=check
    #print(flag,tipo)
    return flag, tipo



def configurar_vnfd(archivo_config):
    """Copia los archivos de configuración dado al archivo de configuracion local para ver sus parametros activos"""
    vnfd_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/vnfd_mapping")
    print("CONFIGURAR VNFD")
    print(archivo_config["cfg_simulador"]["params_general"]["iteracion"])
    print(vnfd_sim["cfg_simulador"]["params_general"]["Iteración"])
    

    vnfd_sim["cfg_simulador"]["params_general"]["Iteración"][0]=archivo_config["cfg_simulador"]["params_general"]["iteracion"]
    vnfd_sim["cfg_simulador"]["params_general"]["Número de celdas"][0]=archivo_config["cfg_simulador"]["params_general"]["n_celdas"]
    vnfd_sim["cfg_simulador"]["params_general"]["Portadora"][0]=archivo_config["cfg_simulador"]["params_general"]["portadora"][0]
    vnfd_sim["cfg_simulador"]["params_general"]["Distancia entre celdas"][0]=archivo_config["cfg_simulador"]["params_general"]["isd"]
    

    vnfd_sim["cfg_simulador"]["params_general"]["Geometría"][0]=archivo_config["cfg_simulador"]["params_general"]["geometria"]
    vnfd_sim["cfg_simulador"]["params_general"]["Radio de Celda"][0]=archivo_config["cfg_simulador"]["params_general"]["radio_cel"] 

    vnfd_sim["cfg_simulador"]["params_general"]["Distribución"][0]=archivo_config["cfg_simulador"]["params_general"]["distribucion"][0]
    vnfd_sim["cfg_simulador"]["params_general"]["Distribución"][1]=float(archivo_config["cfg_simulador"]["params_general"]["distribucion"][1])

    vnfd_sim["cfg_simulador"]["params_general"]["Imagen Potencia"][0]=archivo_config["cfg_simulador"]["params_general"]["imagen"]["resolucion"]
    #
    #
    vnfd_sim["cfg_simulador"]["params_propagacion"]["Modelo Pérdidas de Propagación"][0]=archivo_config["cfg_simulador"]["params_propagacion"]["modelo_perdidas"]
    vnfd_sim["cfg_simulador"]["params_propagacion"]["Parámetros Modelo"][0]=archivo_config["cfg_simulador"]["params_propagacion"]["params_modelo"]
    #[float(archivo_config["cfg_simulador"]["params_propagacion"]["mp1"]), float(archivo_config["cfg_simulador"]["params_general"]["mp2"]), float(archivo_config["cfg_simulador"]["params_general"]["mp3"]),float(archivo_config["cfg_simulador"]["params_general"]["mp4"])]


    flag_desv, tipo_desv=validar_desvanecimiento(archivo_config["cfg_simulador"]["params_propagacion"]["params_desv"])
    #print("check..",tipo_desv)
    vnfd_sim["cfg_simulador"]["params_propagacion"]["Desvanecimiento"][0]=tipo_desv["tipo"]
    vnfd_sim["cfg_simulador"]["params_propagacion"]["Parámetros desvanecimiento"][0]=archivo_config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"]
    #[float(archivo_config["cfg_simulador"]["params_general"]["dp1"]),float(archivo_config["cfg_simulador"]["params_general"]["dp2"]),float(archivo_config["cfg_simulador"]["params_general"]["dp3"]),float(archivo_config["cfg_simulador"]["params_general"]["dp4"])]
    

    vnfd_sim["cfg_simulador"]["params_general"]["Figura de Ruido"][0]=float(archivo_config["cfg_simulador"]["params_general"]["nf"][0])
    vnfd_sim["cfg_simulador"]["params_general"]["Umbral SINR"][0]=float(archivo_config["cfg_simulador"]["params_general"]["ber_sinr"])
    #
    #
    print("views.py: potencias")
    vnfd_sim["cfg_simulador"]["params_balance"]["ptx"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["ptx"])
    vnfd_sim["cfg_simulador"]["params_balance"]["gtx"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["gtx"])
    vnfd_sim["cfg_simulador"]["params_balance"]["ltx"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["ltx"])
    vnfd_sim["cfg_simulador"]["params_balance"]["lrx"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["lrx"])
    vnfd_sim["cfg_simulador"]["params_balance"]["grx"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["grx"])
    #vnfd_sim["cfg_simulador"]["params_balance"]["sensibilidad"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["sensibilidad"])
    vnfd_sim["cfg_simulador"]["params_balance"]["mcl"][0]=float(archivo_config["cfg_simulador"]["params_balance"]["mcl"])
    #antenas
    vnfd_sim["cfg_simulador"]["params_antena"]["Tipo de Antena"][0]=archivo_config["cfg_simulador"]["params_antena"]["tipo"]
    vnfd_sim["cfg_simulador"]["params_antena"]["hpbw"][0]=archivo_config["cfg_simulador"]["params_antena"]["hpbw"]
    vnfd_sim["cfg_simulador"]["params_antena"]["Atenuación Mínima"][0]=float(archivo_config["cfg_simulador"]["params_antena"]["atmin"])
    #vnfd_sim["cfg_simulador"]["params_antena"]["apuntamiento"][0]=int(archivo_config["cfg_simulador"]["params_general"]["apuntamiento"])

    #
    #
    print("views.py: asignacion")
    vnfd_sim["cfg_simulador"]["params_asignacion"]["Tipo"][0]=archivo_config["cfg_simulador"]["params_asignacion"]["tipo"]
    vnfd_sim["cfg_simulador"]["params_asignacion"]["BW"][0]=int(archivo_config["cfg_simulador"]["params_asignacion"]["bw"][0])
    #config["cfg_simulador"]["params_asignacion"]["numerologia"]=float(archivo_config["cfg_simulador"]["params_asignacion"]["numerologia"])
    #config["cfg_simulador"]["params_asignacion"]["bw_guarda"][0]=int(archivo_config["cfg_simulador"]["params_asignacion"]["banda_guarda"])
    vnfd_sim["cfg_simulador"]["params_asignacion"]["Subportadora OFDM"][0]=float(archivo_config["cfg_simulador"]["params_asignacion"]["sub_ofdm"])
    vnfd_sim["cfg_simulador"]["params_asignacion"]["TRAMA OFDM"][0]=float(archivo_config["cfg_simulador"]["params_asignacion"]["trama_total"])
    vnfd_sim["cfg_simulador"]["params_asignacion"]["Símbolo OFDM DL"][0]=float(archivo_config["cfg_simulador"]["params_asignacion"]["simbolo_ofdm_dl"])
    vnfd_sim["cfg_simulador"]["params_asignacion"]["TRAMA OFDM"][0]=float(archivo_config["cfg_simulador"]["params_asignacion"]["frame"])

    
    #cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos")
    cfg.guardar_json(vnfd_sim, target_path="simapp/static/simulador/base_datos/vnfd_mapping")
    print("vies.py")
    print(vnfd_sim)
    print(archivo_config)

#----------------------------END

#--------------------------------------
#--------------------------------------
'''VIEWs'''
#--------------------------------------
#--------------------------------------
# Create your views here.
def home(request):
    '''Index: debe cambiarse a la version del simulador mas reciente'''
    return render(request,'simapp/index/sami-index.html')


def form_demo_sami_v1(request):
    '''Demostracion de formulario.'''
    return render(request,'simapp/form_demo/sami-demo-v1.html')


def futuro(request):
    '''Para mostrar pagina bajo desarrollo'''
    return render(request,'simapp/sami-futuro.html')


def iniciar_simulacion(request):
    '''Inicia la simulacion''' 
    ascii_banner = pyfiglet.figlet_format("SAMI-5G")
    print(ascii_banner)
    cfg_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
    configuracion=cfg.cargar_json_full(target_path=cfg_sim["ruta_activa"])
    #configuracion=cfg.cargar_cfg(target_path="simapp/static/simulador/base_datos")
    if request.method == 'GET':
        try:
            arr = os.listdir()
            print(arr)
        except Exception as ex:
            print(ex)
        #exists = os.path.isfile('qw2ass<z/path/to/file')
        #print(exists)
        print("GET Metodo")
        
        '''***OPTIMIZACION***
        Anotacion de suma importancia:
        Que ocurre cuando el sistema es grande? es decir, con muchos usuarios y muchas celdas?
        La presimulacion se ejecuta como una simulacion y pierde el sentido de efectuarla. Esto
        ocurre debido a que la presimulacion y la simulacion ocurren al mismo tiempo. En la clase no existe
        ninguna diferencia entre ambas. La presimulacion si es diferente en simulador pues usa funciones internas
        configuradas con ese proposito, mas sin embargo la simulacion y todos los detalles tambien se ejecutan.
        
        Existen dos opciones para optimizar la presimulacion e indpendientemente ejecutar la simulacion que es el comportamiento esperado.
        La primera opcion directa y mas facil consiste en que al ejecutar la presimulacion, los datos para ese escenario (1 iteracion) se usen 
        para obtener estadisticas de muestras de valores (valores de potencia, sinr, estadisticas). Esta presimulacion seria la simulacion 0, cuya 
        utilidad puede o no (dependiendo del disenno) usarse en el compendio de simulacion montecarlo para su estudio. E
        Sin embargo, es de suma importancia comprobar logicamente el flujo de esta operacion, debido que en presimulacion, hasta el modelo del
        canal, los valores originales de distancia y otros se mantienen intactos, luego estos cambian para generar las graficas correspondientes.

        Para comprobar basta con imprimir la informacion de esa presimulacion.

        La segunda opcion es mas compleja e implica tambien cambios profundos de disenno,
        cuya solucion planteada puede agregarse un parametro adicional que indique que la simuacion
        no es una completa sino una con datos custom de pruebas. En este caso, los calculos de potencia, sinr, trhougput no se generan, 
        y la simulacion de montecarlo este parametro se desactiva (o no dependiendo de la logica implementada)
        para que la primera simulacion corresponda.

        Escenario 1:
            simulacion 0
            Hay perdida de datos.
            Se generan estadisticas simples de simulacion (datos: 56%, 40%, 100%, 100/399, etc)

            MONTECARLO: estadisticas complejas (graficas)

        Escenario 1.2:
            imulacion 0 como simulacion 1 de montecarlo.
            No hay perdida de datos.
            Es necesario crear una copia de presim antes de que sea modificada.
        Esecenario 2:
            Separar los calculos, hasta el modelo del canal y no calcular lo sucesivo.
                implica perder los primeros datos (generacion de usuarios)
        '''
        presim=samiv1.Simulador(tipo="presimulacion")
        #limpiar rutas.
        presim.graficas_disponibles_dic={}

        #presim_graphs=presim.graficas_disponibles
        #EN SIMULACION, DESACTIVAR LA GENERACION DE IMAGENES.
    
        #si iteracion>1 and iteracion<5, ejecutar tipo="simulacion"
            #mensaje: no hay suficientes tomas para crear estadisticas.
                #fordward to tablas (datos por simulacion)
        #si iteracion>=5, ejecutar tipo="montecarlo"
        iteracion=configuracion["cfg_simulador"]["params_general"]["iteracion"]
        if iteracion>=1 and iteracion<10:
            print("[view.gui]:Montecarlo no disponible para iteracion<10")
            #go to 
            #sim=samiv1.Simulador(tipo="simulacion")
            
            #step1: en presim, antes del cambio de muestra, 
                #copiar info de simulacion.
            #clean memory
            presim=0
            #presim.info_sinr()
            '''Falta modulo que guarda estos datos, debe almacenarse en una ruta de path'''


        elif iteracion>=10:
            print("[view.gui]:Montecarlo activado, porfavor espere...")
            montecarlo=samiv1.Simulador(tipo="montecarlo")
        
        #reload enviroment para poder ver la nueva entrada en seleccionar escenario.
        fname="sami/wsgi.py"
        try:
            os.utime(fname, None)  # Set access/modified times to now
        except OSError:
            pass  # File does not exist (or no permission)


        
    return render(request,'simapp/configuracion_datos/sami-iniciar-sim.html')



def ejecutar_parametros(request):
    '''Punto de control: se observan los parametros, se decide iniciar simulacion
    o corregirlos con las opciones disponibles.'''
    #configuracion=cfg.cargar_cfg(target_path="simapp/static/simulador/base_datos")
    #simapp/static/simulador/base_datos/escenarios/test_ci_1.json
    cfg_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
    configuracion=cfg.cargar_json_full(target_path=cfg_sim["ruta_activa"])

    config1=configuracion["cfg_simulador"]["params_general"]
    config2=configuracion["cfg_simulador"]["params_propagacion"]
    config3=configuracion["cfg_simulador"]["params_balance"]
    config4=configuracion["cfg_simulador"]["params_antena"]
    config5=configuracion["cfg_simulador"]["params_asignacion"]

    return render(request,'simapp/configuracion_datos/sami-ejecutar-parametros.html', {"cfg1":config1, 
    "cfg2":config2, "cfg3":config3, "cfg4":config4, "cfg5":config5 })


def ver_parametros(request):
    '''Punto de control: se observan los parametros, se decide iniciar simulacion
    o corregirlos con las opciones disponibles.'''
    #configuracion=cfg.cargar_cfg(target_path="simapp/static/simulador/base_datos")
    #simapp/static/simulador/base_datos/escenarios/test_ci_1.json
    vnfd_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/vnfd_mapping")
    #configuracion=cfg.cargar_json_full(target_path=cfg_sim["ruta_activa"])
    cfg_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")

    config1=vnfd_sim["cfg_simulador"]["params_general"]
    config2=vnfd_sim["cfg_simulador"]["params_propagacion"]
    config3=vnfd_sim["cfg_simulador"]["params_balance"]
    config4=vnfd_sim["cfg_simulador"]["params_antena"]
    config5=vnfd_sim["cfg_simulador"]["params_asignacion"]

    ruta_activa=cfg_sim["ruta_activa"].split("/")[-1]
    return render(request,'simapp/configuracion_datos/sami-parametros.html', {"cfg1":config1, 
    "cfg2":config2, "cfg3":config3, "cfg4":config4, "cfg5":config5, "ruta_act":ruta_activa })

def ver_presim(request):
    #se separa el archivo de path debido a que genera problemas en modo debug
    configuracion=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_gui")
    imagenes_disp=configuracion["presim_graphs"]
    #print(imagenes_disp)
    return render(request,'simapp/resultados/sami-presim-graficas.html', {"img_disp":imagenes_disp})


def ver_sim(request):
    configuracion=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_gui")
    conf_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
    configuracion_base=cfg.cargar_json_full(target_path=conf_sim["ruta_activa"])
    iteracion=configuracion_base["cfg_simulador"]["params_general"]["iteracion"]
    imagenes_disp=configuracion["montecarlo_graphs"]
    #cambia a las graficas de simulacion
    #print(imagenes_disp)
    if iteracion >= 1 and iteracion < 10:
        return render(request,'simapp/resultados/sami-sim-graficas-empty.html')
    else:
        return render(request,'simapp/resultados/sami-sim-graficas.html', {"img_disp":imagenes_disp})


#FORMULARIOS V1

def seleccionar_escenario(request):
    '''Selecciona un escenario para simular'''
    config_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
    vnfd_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/vnfd_mapping")

    rutas_disponibles=config_sim["rutas_configuracion"]    
    form=FormSeleccion()

    if request.method == 'POST':
        form=FormSeleccion(request.POST)
        print("\nHA OCURRIDO UN POST Seleccion", request.POST)
        if form.is_valid():
            print("[OK]-Formulario seleccion Aceptado")
            contenido=form.cleaned_data
            print("clase django", contenido)

            config_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
            config_sim["ruta_activa"]="{}".format(contenido["escenario_opciones"].replace(" ","_"))
            # 
            configurar_vnfd(cfg.cargar_json_full(config_sim["ruta_activa"]))
            #     
            cfg.guardar_json(config_sim, target_path="simapp/static/simulador/base_datos/config_sim")
        else:
            print("Error")
        return redirect('ejecutar_parametros/')
    return render(request,'simapp/configuracion_datos/sami-form-escenarios.html', {"form_data":form})




def form_compacto(request):
    '''Implementacion de 4 fases en 1 para agilizar la simulacion.'''

    form=FormCompacto()
    if request.method == 'POST':
        form=FormCompacto(request.POST)
        print("\nHA OCURRIDO UN POST Compacto", request.POST)
        if form.is_valid():
            print("[OK]-Formulario 1 Aceptado")
            contenido=form.cleaned_data
            print("clase django", contenido)

            config=cfg.cargar_cfg(target_path="simapp/static/simulador/base_datos")

            config_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
            rutas_=config_sim["rutas_configuracion"]
            rutas_[contenido["nombre_archivo"]]="simapp/static/simulador/base_datos/escenarios/{}.json".format(contenido["nombre_archivo"].replace(" ","_"))
            config_sim["ruta_activa"]="simapp/static/simulador/base_datos/escenarios/{}.json".format(contenido["nombre_archivo"].replace(" ","_"))
            print("ruta activa!!!!! \n",config_sim)

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
            if flag_imagen:
                print("imagen activado, desactivar iteraciones.")
                #config["cfg_simulador"]["params_general"]["iteracion"]=1
            config["cfg_simulador"]["params_general"]["imagen"]["resolucion"]=contenido["pixeles"]
            #
            #
            config["cfg_simulador"]["params_propagacion"]["modelo_perdidas"]=contenido["modelo_perdidas"]
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][0]=float(contenido["mp1"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][1]=float(contenido["mp2"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][2]=float(contenido["mp3"])
            config["cfg_simulador"]["params_propagacion"]["params_modelo"][3]=float(contenido["mp4"])

            flag_desv, tipo_desv=validar_desvanecimiento(contenido["params_desv"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["display"]=flag_desv
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["tipo"]=tipo_desv
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][0]=float(contenido["dp1"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][1]=float(contenido["dp2"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][2]=float(contenido["dp3"])
            config["cfg_simulador"]["params_propagacion"]["params_desv"]["params"][3]=float(contenido["dp4"])

            config["cfg_simulador"]["params_general"]["nf"][0]=float(contenido["nf"])
            config["cfg_simulador"]["params_general"]["ber_sinr"]=float(contenido["ber_sinr"])
            #
            #
            print("views.py: potencias")
            config["cfg_simulador"]["params_balance"]["ptx"]=float(contenido["ptx"])
            config["cfg_simulador"]["params_balance"]["gtx"]=float(contenido["gtx"])
            config["cfg_simulador"]["params_balance"]["ltx"]=float(contenido["ltx"])
            config["cfg_simulador"]["params_balance"]["lrx"]=float(contenido["lrx"])
            config["cfg_simulador"]["params_balance"]["grx"]=float(contenido["grx"])
            #config["cfg_simulador"]["params_balance"]["sensibilidad"]=float(contenido["sensibilidad"])
            config["cfg_simulador"]["params_balance"]["mcl"]=float(contenido["mcl"])
            #antenas
            config["cfg_simulador"]["params_antena"]["tipo"]=contenido["tipo_antena"]
            config["cfg_simulador"]["params_antena"]["hpbw"]=contenido["hpbw"]
            config["cfg_simulador"]["params_antena"]["atmin"]=float(contenido["atmin"])
            config["cfg_simulador"]["params_antena"]["apuntamiento"][0]=int(contenido["apuntamiento"])

            #
            #
            print("views.py: asignacion")
            config["cfg_simulador"]["params_asignacion"]["tipo"]=contenido["tipo_asignacion"]
            config["cfg_simulador"]["params_asignacion"]["bw"][0]=int(contenido["bw"])
            #config["cfg_simulador"]["params_asignacion"]["numerologia"]=float(contenido["numerologia"])
            #config["cfg_simulador"]["params_asignacion"]["bw_guarda"][0]=int(contenido["banda_guarda"])
            config["cfg_simulador"]["params_asignacion"]["sub_ofdm"]=float(contenido["subportadora"])
            config["cfg_simulador"]["params_asignacion"]["trama_total"]=float(contenido["trama"])
            config["cfg_simulador"]["params_asignacion"]["simbolo_ofdm_dl"]=float(contenido["simbolos"])
            config["cfg_simulador"]["params_asignacion"]["frame"]=float(contenido["frame"])
            #cfg.guardar_cfg(config, target_path="simapp/static/simulador/base_datos")
            
        
            cfg.guardar_json(config_sim, target_path="simapp/static/simulador/base_datos/config_sim")
            cfg.guardar_json_full(config, target_path=config_sim["ruta_activa"])
            configurar_vnfd(config)
            #reload enviroment para poder ver la nueva entrada en seleccionar escenario.
            fname="sami/wsgi.py"
            try:
                os.utime(fname, None)  # Set access/modified times to now
            except OSError:
                pass  # File does not exist (or no permission)
        return redirect('ejecutar_parametros/')
    return render(request,'simapp/configuracion_datos/sami-form-compacto.html', {"form_data":form})
    #return render(request,'simapp/form_v1/sami-form-a4.html', {"form_data":form} )



def seleccionar_comparacion(request):
    '''Selecciona dos escenarios simulados'''

    form=FormComparacion()

    if request.method == 'POST':
        form=FormComparacion(request.POST)
        print("\nHA OCURRIDO UN POST Seleccion de comparacion", request.POST)
        if form.is_valid():
            print("[OK]-Formulario seleccion Aceptado")
            contenido=form.cleaned_data
            print("clase django", contenido)
            
            config_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")
            config_sim["rutas_comparacion"]["ruta_principal"]="{}".format(contenido["escenario_opcion_1"])
            config_sim["rutas_comparacion"]["ruta_secundaria"]="{}".format(contenido["escenario_opcion_2"])
            #    
            cfg.guardar_json(config_sim, target_path="simapp/static/simulador/base_datos/config_sim")
            
        else:
            print("Error")
        return redirect('resultados_comparacion/')

    return render(request,'simapp/estadisticas/sami-form-comparar-escenarios.html', {"form":form})



def resultados_comparacion(request):
    '''Muestra uno a uno, las imagenes renderizadas de simulacion'''
    # _1 presimulacion
    # _2 montecarlo
    config_sim=cfg.cargar_json(target_path="simapp/static/simulador/base_datos/config_sim")

    rutap_1=config_sim["rutas_comparacion"]["ruta_principal"]+"/presim/"
    rutap_2=config_sim["rutas_comparacion"]["ruta_principal"]+"/montecarlo/"

    imagenes_principal_1 = os.listdir(rutap_1)
    imagenes_principal_1 = [rutap_1.replace('simapp/static/','')+i for i in imagenes_principal_1]

    imagenes_principal_2 = os.listdir(rutap_2)
    imagenes_principal_2 = [rutap_2.replace('simapp/static/','')+i for i in imagenes_principal_2]
    
    #
    rutasec_1=config_sim["rutas_comparacion"]["ruta_secundaria"]+"/presim/"
    rutasec_2=config_sim["rutas_comparacion"]["ruta_secundaria"]+"/montecarlo/"

    imagenes_secundaria_1 = os.listdir(rutasec_1)
    imagenes_secundaria_1 = [rutasec_1.replace('simapp/static/','')+i for i in imagenes_secundaria_1]
    imagenes_secundaria_2 = os.listdir(rutasec_2)
    imagenes_secundaria_2 = [rutasec_2.replace('simapp/static/','')+i for i in imagenes_secundaria_2]

    #imagenes_principal=imagenes_principal_1+imagenes_principal_2
    #imagenes_secundaria=imagenes_secundaria_1+imagenes_secundaria_2

    imagenes_presim=[]
    imagenes_montecarlo=[]
    for prin, sec in zip(imagenes_principal_1,imagenes_secundaria_1):
        imagenes_presim.append(prin)
        imagenes_presim.append(sec)
    
    for pprin, ssec in zip(imagenes_principal_2,imagenes_secundaria_2):
        imagenes_montecarlo.append(pprin)
        imagenes_montecarlo.append(ssec)
    
    print("FROM DJANGO ...................")
    print(imagenes_presim)
    print("FROM DJANGO ...................")
    print(imagenes_montecarlo)

    return render(request,'simapp/estadisticas/sami-sim-graficas-comparacion.html',{"img_presim":imagenes_presim, "img_mont":imagenes_montecarlo})

#AUXILIAR Y PRUEBAS
