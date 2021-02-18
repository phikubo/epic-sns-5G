import numpy as np
import math
import os


class Modulacion:
    '''Clase: asigna prb por usuario, calcula matriz de interferencia.'''
    
    def __init__(self, params_cfg, generacion, params):
        # 0 mientras no haya configuracion
        self.cfg_plan = params_cfg
        #generacion disponible 5G. En el futuro variantes o 6G.
        self.generacion = generacion
        # lista que contiene parametros extra o para agregar funcionalidad.
        self.lista_params = params

        # constantes
        self.lst_sinr_objetivo = [-9.533495583, -5.248540551, -0.7750688964, 2.511321215, 4.422894404, 6.335825987,
            7.510369502, 9.543669017, 11.44647253, 13.42371711, 15.27114189, 16.62792018, 18.68554795, 20.777354, 22.26950728]
        self.lst_tasa_codificion = [
            78, 193, 449, 378, 490, 616, 466, 567, 666, 772, 873, 711, 797, 885, 948]
        self.lst_modulacion = [2, 2, 2, 4, 4, 4, 6, 6, 6, 6, 6, 6, 8, 8, 8]

        # auxiliar
        self.sinr_inferior = 0
        self.sinr_superior = 0
        self.tasa_inferior = 0
        self.mod_inferior = 0
        # OUTPUT
        self.arr_tasa = []
        self.arr_modulacion = []
    

    def asignar_tasa_modulacion_5G(self,sinr_in):
        '''segun la tasa y modulacion dado un valor unico de sinr.'''
        # es posible cambiar las longitudes del slicing para limitar la accion del modulo segun los datos.
        sinr_tar = self.lst_sinr_objetivo[:]
        tasa_tar = self.lst_tasa_codificion[:]
        mod_tar = self.lst_modulacion[:]
        # flag para verificar si sinr_in esta en el limite superior y asigna maximo
        verificar_superior = False
        # flag para verificar si sinr_in es menor al limite inferior y desconecta
        verificar_inferior = False

        for ind, sinr_ in enumerate(sinr_tar):
            if sinr_in >= 22.26950728:
                print("{debug}:subir")
                verificar_superior = True
                sinr_in = 22.26950727
            elif sinr_in < -9.533495583:
                verificar_inferior = True
            else:
                pass

            res = sinr_-sinr_in
            if res > 0:
                print("comparar", sinr_)
                print("con ", sinr_in)
                print("resta", sinr_-sinr_in)
                print("---")
                inferior = ind-1
                superior = ind
                sinr_inferior = sinr_tar[inferior]
                sinr_superior = sinr_tar[superior]
                print("indice down {}, up {}".format(inferior, superior))
                print("valores: ", sinr_inferior, sinr_superior)
                break
        # verificamos que se encuentra en el limite superior de la tabla, por tanto obtiene el mayor valor de tasa.
        if verificar_superior:
            # selecciona tasa mas alta
            tasa_inferior = tasa_tar[superior]
            mod_inferior = mod_tar[superior]
            # se encuentra en el valor maximo, ambos son iguales.
            sinr_inferior=sinr_superior
        else:
            # si no esta en un limite, siempre toma el valor mas bajo
            tasa_inferior = tasa_tar[inferior]
            mod_inferior = mod_tar[inferior]


        if verificar_inferior:
            mod_inferior = -300
            tasa_inferior = -300
            sinr_superior = -300
            sinr_inferior = -300
        else:
            pass
            
        # tambien se puede obtener los demas valores, pero en esta verion no es necesario.
        return tasa_inferior, mod_inferior
    

    def arreglos_tasa_modulacion(self, arr_sinr):
        '''Genera el arreglo de tasa y modulacion.'''        
        if self.generacion=="5G":
            for sinr_in in arr_sinr:
                tasa,modulacion=self.asignar_tasa_modulacion_5G(sinr_in)
                self.arr_tasa.append(tasa)
                self.arr_modulacion.append(modulacion)
        elif self.generacion=="4G":
            #no disponible por diseño
            pass
            
        elif self.generacion=="5.5G":
            #[futuro]: adicionar en futuros trabajos de grado.
            pass
            
        elif self.generacion=="6G":
            #[futuro]: adicionar en futuros trabajos de grado.
            pass




def prueba_modulacion():
    # prueba de modulaciones dado sinr
    # asignar modulacion segun sinr
    sinr_down, sinr_up, tasa, modulacion = asignar_tasa_modulacion(sinr_in=23)
    if modulacion == 2:
        modulacion = "qpsk"
    elif modulacion == 4:
        mudulacion = "16qam"
    elif modulacion == 6:
        modulacion = "64qam"
    elif modulacion == 8:
        modulacion = "256qam"
    print("tasa {}, modulacion {}\nsinr_up {}, sinr_down {}.".format(tasa, modulacion, sinr_up, sinr_down))



def asignar_tasa_modulacion(sinr_in):
    '''obtiene limites de sinr, tasa de codificaion y orden de modulacion'''
    lista_sinr_objetivo_original = [-9.533495583, -5.248540551, -0.7750688964, 2.511321215, 4.422894404, 6.335825987,
                                    7.510369502, 9.543669017, 11.44647253, 13.42371711, 15.27114189, 16.62792018, 18.68554795, 20.777354, 22.26950728]
    lista_tasa_codificion_original = [
        78, 193, 449, 378, 490, 616, 466, 567, 666, 772, 873, 711, 797, 885, 948]
    lista_modulacion_original = [2, 2, 2, 4, 4, 4, 6, 6, 6, 6, 6, 6, 8, 8, 8]
    # -1-no conectado
    # 2-qpsk
    # 4-16qam
    # 6-32qam
    # 8-64qam

    # sinr_tar=lista_sinr_objetivo_original[3:]
    # tasa_tar=lista_tasa_codificion_original[3:]

    sinr_tar = lista_sinr_objetivo_original[:]
    tasa_tar = lista_tasa_codificion_original[:]
    mod_tar = lista_modulacion_original[:]
    # verifica si sinr_in esta en el limite superior y asigna maximo
    verificar_superior = False
    # verifica si sinr_in es menor al limite inferior y desconecta
    verificar_inferior = False

    for ind, sinr_ in enumerate(sinr_tar):
        if sinr_in >= 22.26950728:
            print("{debug}:subir")
            verificar_superior = True
            sinr_in = 22.26950727
        elif sinr_in < -9.533495583:
            verificar_inferior = True
        else:
            pass

        res = sinr_-sinr_in
        if res > 0:
            print("comparar", sinr_)
            print("con ", sinr_in)
            print("resta", sinr_-sinr_in)
            print("---")
            inferior = ind-1
            superior = ind
            sinr_inferior = sinr_tar[inferior]
            sinr_superior = sinr_tar[superior]
            print("indice down {}, up {}".format(inferior, superior))
            print("valores: ", sinr_inferior, sinr_superior)
            break
    # verificamos que se encuentra en el limite superior de la tabla, por tanto obtiene el mayor valor de tasa.
    if verificar_superior:
        # selecciona tasa mas alta
        tasa_inferior = tasa_tar[superior]
        mod_inferior = mod_tar[superior]
        # se encuentra en el valor maximo
        sinr_inferior=sinr_superior
    else:
        tasa_inferior = tasa_tar[inferior]
        mod_inferior = mod_tar[inferior]


    if verificar_inferior:
        mod_inferior = -300
        tasa_inferior = -300
        sinr_superior = -300
        sinr_inferior = -300
    else:
        pass
    print(mod_inferior, tasa_inferior)

    return sinr_inferior, sinr_superior, tasa_inferior, mod_inferior


def calcular_tbs_ber(n_rb,modulacion,tasa,arreglo_mimo,sym_ofdm,scs_ofdm):
    '''Funcion para calcular tbs, dado la modulacion y tasa de bits.
    Numero de bloques de recursos asignados al PBCH donde el DM-RS es el canal de transmision y consume 24 bloques.'''
    # numeros
    constant_dmrs=13
    const_oh=5
    const_bler=0.1 #fijo al 10%

    # [?]
    n_rep=scs_ofdm*sym_ofdm-constant_dmrs-const_oh #12*12 - 13 - 5 ?
    # [?]
    n_re=min(156,n_rep)*n_rb #porque 156?
    # [?]
    n_info=n_re*(tasa/1024)*modulacion*arreglo_mimo #que es esto?

    if n_info <= 3824:
        n=max(3,math.floor(math.log2(n_info)-6))
        n_infop=max((24.2**n)*math.floor(n_info/2**n))
    elif n_info >3824:
        # [?]
        n=math.floor(math.log2(n_info-24))-5 #por que 5?
        n_infop=max(3840,(2**n)*round((n_info-24)/2**n))
    else:
        pass

    # [?] r->tasa, ya esta divido en 1024 en [?-3]
    # r_ref=r/1024
    r_ref=tasa/1024

    # [!!!]: CONDICION NO COMPARA VARIABLES IGUALES.
    if r_ref <= 0.25:
        # [?]: porque 3816?
        c= math.ceil((n_infop+24)/3816)
        # [?]
        tbs=8*c*math.ceil((n_infop+24)/(8*c))-24 #por que +24,-24
    # [???]: por que la compara 0.25 con 8424 en diferentes variables
    elif n_info > 8424:
        c=math.ceil(n_infop+24/3816)
        tbs=8*c*math.ceil((n_infop+24)/(8*c))

    # [???]: que condincion es esta?. No tiene sentido... teniendo en cuenta que el primer if
    # y el segundo elif, no son las mismas variables, entonces este else
    # a que condicion hace referencia?
    else:
        # [?]:por que 24?
        tbs=8*math.ceil((n_infop+24/8))-24

    ber = 1- (1-const_bler)**(1/tbs)
    return tbs, ber

    '''
    # paso1a cuantizar nre
    # paso2a calcular ninfo
    # paso2b:

        if ninfo<=3824:
            # paso3->tbs_tablas
        else:
            # paso4
            # calcular n
            # quantizar ninfo_p
            
            if r<=1/4:
                # calcular tbs1
            else:
                if ninfo_p>8424:
                    # calcular tbs2
                else:
                    # calcular tbs3
    '''
                





def calcular_throughput(n_rb,modulacion,tasa,arreglo_mimo,numerologia):
    '''Calcular el throuhgput dado valores de entrada'''
    # v_mimo,m_mod,r_max,n_rb,numerologia

    # [?]: por que se calcula? esto ya se calculo en Planificador
    trama=10**(-3)/(14*2**numerologia)
    # La cantidad de subportadoras OFDM es fija y es de 12
    # [?] por que se repite?
    sub_ofdm=12

    # que es esto?
    scaling_factor=[1,0.8,0.75,0.4]

    # [???]: como se relaciona con const_oh del calculo de tbs,ber?
    oh=[0.14,0.18]
    v_oh=(1-oh[1])

    # [!!!]: por que se selecciona scaling_factor[1]?
    print(arreglo_mimo, modulacion, scaling_factor[0], tasa, n_rb, sub_ofdm, trama, v_oh)
    throughput_user=10**(-6)*arreglo_mimo*modulacion*scaling_factor[0]*(tasa/1024)*(n_rb*sub_ofdm/trama)*v_oh
    return throughput_user


def definir_flujo():
    # define las variables de prueba y el flujo
    constant_dmrs=13
    constant_oh=5
    arreglo_mimo=1
    n_ofdm=12
    n_rb=100
    sinr_in=10
    sym_ofdm=12
    scs_ofdm=12

    case_use=["URRLC", "mmtc", "ebmm"]
    numerologia=[0,1,2,3]

    numerologia=numerologia[1]

    # [?]: no se usa. Por que definir entonces?
    case_use=case_use[0]

    # asignar modulacion dado sinr
    sinr_down, sinr_up, tasa, modulacion = asignar_tasa_modulacion(sinr_in)
    # calcualr tbs
    # traduccion de variables
    # (modulacion,m_mod)
    # (tasa, r_max)
    # (arreglo_mimo, v_mimoprint(modulacion)
    # calcualr tbs, ber
    tbs,ber=calcular_tbs_ber(n_rb,sym_ofdm,scs_ofdm,modulacion,tasa,arreglo_mimo)

    # calcular thoughput
    # [!!!!!!!]: por que en este calculo no se usa tbs, ber?, cual es el punto de calcularlo?
    throughput=calcular_throughput(n_rb,modulacion,tasa,arreglo_mimo,numerologia)

    print("thouhgput: {}".format(throughput))


if __name__ == "__main__":
	# Prototipo:
	# prueba_modulacion()
    definir_flujo()
    # si todo funciona, felicidades ya podemos graduarnos alv.
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")
