import numpy as np
import math
import os

class Modulacion:
	'''Clase: asigna prb por usuario, calcula matriz de interferencia.'''
	def __init__(self, params_cfg, params_cfg_gen, params):
		self.cfg_plan=params_cfg
		self.cfg_gen=params_cfg_gen
		#numero de usuarios por celda
		self.mapa_conexion=params[0]
		#self.dim_pot_r=params[1]
		#self.aux_ones_interf=np.ones(params[1])

		#output:
		self.asignacion=0 #por usuario

		#self.inicializar_tipo()

		#self.numerologia=[0,1,2,3]
		#self.cp_ofdm=['Normal','Extendido']
		#self.format_slot=['D','U','F']
		#self.case_use=['mMTC','eBMM','URLLC']

		#self.configurar_tipo_asignacion()
		#self.calcular_tipo_asignacion()
 
def asignar_ber_caso_uso(case_use):
    ber_modqam=(10**(-3) if case_use=='ebmm' else 10**(-5) if case_use=='urrlc' else 10**(-1))
    return ber_modqam



def asignar_snr_lim_urrlc():
    pass
def asignar_snr_lim_mmtc():
    pass
def asignar_snr_lim_ebmm():
    pass
def asignar_modulacion_mqam(snr_in,case_use,desv):
    #Las modulaciones dependen de la SINR y la BER objetivo que se hace presente en el tipo de caso de uso a utilizar
    #cada caso de uso este especificado para soportar cierta cantidad de errores debido al tipo de servicio que se espera
    snr_in=float(snr_in)
    #https://arxiv.org/pdf/1804.05057.pdf
    # eMBB requiere tasas de datos altas pero no especifica la confiabilidad de los datos recibidos, el tipo de informacion
    # que es enviada es considerada como datos o audio, para este caso la BER objetivo es considerada de 10**-3.
    ber_ebmm=10**(-3)
    #URLLC requiere de latencias muy bajas y control de la informacion, sopotando baja eficiencia espectral, y tiempos 
    #transmision mas cortos, razon por la cual la BER objetivo que se espera de estos servicios es mas alta, 
    #el tipo de infomacion que se espera enviar es video live stream, paquetes de datos con confiabilidad y sin retardo
    #la BER objetivo para este caso de uso considerada es de 10**-5
    ber_urllc=10**(-5)
    #mMTC es el caso de uso con menor exigencia encuanto a recursos de la red y confiabilidad de los datos, lo mas importante
    #para este caso de uso es el uso eficiente de bloques de recursos para conectar la mayor cantidad de dispositivos a la red
    #de esta manera no es necesario usar numerologias altas, la informacion que es enviada es considerada como datos  tipo texto
    #y la informacion no tiene que tener un tiempo corto de transmision corto a menos que sean datos en tiempo real, que 
    # de igual manera la latencia permitida es alta y la confiabilidad de que la informacion llegue es media, la codificacion
    # de canal y de linea darian en soporte necesario para la transmision de esta informacion, la BER objetivo considerada 
    # para este tipo de servicios tipo IoT seria de 10**-1 para servicios como M2M y D2D la BER objetivo aumenta hasta 
    #10**-3
    ber_mmtc= 10**(-1)
    '''La varianza de interferencia es considerada como el aumento de la SNR segun los bloques de recursos usados en otras 
    estaciones base, con el fin de tener una interferencia mas real a la hora de implementar el simulador, evitando el numero
    de desconexiones debido baja SINR'''
    ber_modqam=asignar_ber_caso_uso(case_use)
    #Para encontrar los diferentes niveles de SNR necesarios al incorporar los desvanecimientos requeridos como lo son  
    #el desvanecimiento lento y rapido, ademas de tener la incorporacion de este mismo desvanecimiento tipo mixto
    #Incorporando la codificacion LDCP para cada unao de los desvanecimientos lo que encontramos es una relacion de 
    #eficiencia para la transmision, estos valores son tomados del siguiente link
    #https://www.researchgate.net/publication/286678997_Performance_Analysis_of_LDPC_Codes_on_Different_Channels
    #Esta codificacion es considerada como la FEC o Correccion de errores hacia delante.}
    #NOTA: Segun las lecturas el slow fading o shadow fading puede considerarse como el AWGN debido a que su ruido es 
    #correalcionado de igual manera al modelo de perdidas de propagacion.
    """"
    segun el valor de la BER por escenario, y segun las curvas generadas para la evaluacion de desempeño de LDCP con 
    diferentes modelos del canal con desvaneimiento lento, rapido y mixto.
    """
    snr_ber_ebmm=6
    snr_ber_urrlc=8
    snr_ber_mmtc=2
    snr_ninguno=[6.33,7.511,2.511] 
    #los parametros anteriores son tomados sin ningun tipo de desvanecimiento solo las perdidas requeridas. valores en dB
    #rapido---------------------------------------------------------------------------
    snr_rapido_ebmm=3
    snr_rapido_urrlc=5
    snr_rapido_mmtc=0
    snr_rapido=[3,5,0]
    #mixto---------------------------------------------------------------------------
    snr_mixto_ebmm=2
    snr_mixto_urrlc=4
    snr_mixto_mmtc=-1
    snr_mixto=[2.33,4.51,-1.49]
    #lento----------------------------------------------------------------------------
    snr_lento_ebmm=4
    snr_lento_urrlc=6
    snr_lento_mmtc=1
    snr_lento=[4.33,6.511,1.51]
    ## Teniendo estos valores podemos tener un valor promedio de cuanto disminuye o aumenta la snr en favor a la 
    # codificacion LDPC contra el dosvanecimiento.
    lim_inf_snr=(snr_lento if desv=='lento' else snr_rapido if desv=='rapido' else snr_mixto)
    """
    La seleccion de la modulacion es escogida segun la tabla 
    """
    #La tasa de codificacion necesaria para el sistema escogida, tasas de 1/3 son mas robustas pero introduce mas redundancia
    #en el sistema, para ordenes mas altos donde es necearia transmitir mas informacion, la redundancia no es necesaria
    # asi que codificaciones entre mas cerca a 1 son mejores. pero las que tiene mejor relacion de SNR son de 1/3 
    modulacion_mqam=[4 if (snr_in >= float(lim_inf_snr[0]) or snr_in < 8) and ber_modqam==10**(-3) else None]
    print(lim_inf_snr[0],ber_modqam)
    print(modulacion_mqam)
    #modulacion_mqam=[4 if (snr_in >= lim_inf_snr[1] or snr_in < 8.3) and ber_modqam=='urrlc' else None]
    #modulacion_mqam=[4 if (snr_in >= lim_inf_snr[2] or snr_in < 5.5) and ber_modqam=='mmtc' else None]
    ##
    #
    ##
    #modulacion_mqam=[6 if (snr_in >= 8 or snr_in<11) and ber_modqam=='ebmm' else None]
    #modulacion_mqam=[6 if (snr_in >= 8.3 or snr_in<11.4) and ber_modqam=='urrlc' else None]
    #modulacion_mqam=[6 if (snr_in >= 5.5 or snr_in<10) and ber_modqam=='mmtc' else None]
    ##
    #
    ##
    #modulacion_mqam=[8 if (snr_in  >= 11 or snr_in<14 ) and ber_modqam=='ebmm' else None]
    #modulacion_mqam=[8 if (snr_in >= 11.4 or snr_in<14.3) and ber_modqam=='urrlc' else None]
    #modulacion_mqam=[8 if (snr_in >= 9.8 or snr_in<13.5) and ber_modqam=='mmtc' else None]
    return modulacion_mqam
    
def evaluar_lim_inf_snr(snr_in,lim_snr):
    if (snr_in >= lim_snr[0]):
        return True 
    else :
        return False 
def evaluar_lim_snr_sup_snr(snr_in,lim_snr):
    if (snr_in < lim_snr[1]):
        return True 
    else :
        return False 
    pass    
def asignar_lim_snr(sinr_cqi,desv):
    lista_cqi=[]
    pass

def tabla_cqi(desv):    
    
    pass
def asignar_r_max(m_modulacion):
    
    r_max=[658,873,948]
    if m_modulacion==4:
        return r_max[0]
    elif m_modulacion==6:
        return r_max[1]
    elif m_modulacion==8:
        return r_max[2]
    else:
        pass
def throughput():
    """
    Los parametros para asignar el throughput son especificados en TS 38.306
    https://www.etsi.org/deliver/etsi_ts/138300_138399/138306/15.03.00_60/ts_138306v150300p.pdf
    estos parametros ya son designados por el standar y solo haremos algunas aclaraciones y justificaciones de estos valores
    """
    sinr_obtenida=5
    tipo_desv='mixto'
    case_use='urrlc'
    n_rb_sistem=264
    #El numero de capas MIMO usadas en el DL lo encontramos sabiendo el numero de arreglos de antena, segun tr 38.306
    #el numero maximo de capas para el DL en 5g NR esta en el orden de 8 el cual es el numero maximo de antemas en transmision
    # digamos que el numero maximo de elementos de antena es de 8x8 osea 64 elementos de antena dependiendo de como distribuyamos
    # esas capas y segun los arrelgos de antena por ejemplo 8x2 tendriamos 4 capas MIMO disponibles como el maximo arreglo de antena 
    # que se puede generar distribuyendo los elementos de antena que contempla 38.306 para el release 14 es de 8 capas 
    # y para el release 15 no ha cambiado se considera el numero maximo de arreglos de antena de este mismo valor
    n_cap_mimo=[2,4,8]
    #Como ya se explico antes el orden de la modulacion va en relacion directa con la cantidad de bits transmitidos
    # esta relacion es considarada como el orden de modulacion que satisface la tasa de bits
    # a transmitir segun las tablas de MCS para el PDSCH en TS 38.214 para QAM y los valores van  
    # desde 16 hasta 256 donde 256 es la maxima modulacion considerada para el DL
    """"
    los valores asignados para las modulaciones estan consignadas en la tabla 5.1.3.2 de TS 38.214
    de los cuales obtendremos el valor de tasa de datos maxima segun cada modulacion 

        Para orden de modulacion 4 Rmax es de 658
        Para orden de modulacion 6 Rmax es de 873
        Para orden de modulacion 8 Rmax es de 948
    """
    m_mod=asignar_modulacion_mqam(sinr_obtenida,case_use,tipo_desv)
    r_max=asignar_r_max(m_mod)
    numerologia=3
    #Para el factor de escala se tienen ciertos valores preestablecidos por TS 38.306 Aunque el valor por defecto es 1
    """
    Esto se debe a que el factor de escala esta realcionado con las frecuencias portadoras de bandas agreagadas y nos referimos
    es a las portadoras agregadas o CA (Carry Agregation) o CC (Components Carry) donde el uso de mas portadoras afecta la velocidad real 
    de transmision de datos, PERO que en este caso no es determinante ya que solo trabajaremos sobre una frecuencia 
    portadora donde nuestro valor por defecto de factor de escala es de 1

    los posibles valores a tomar segun la cantidad de portadoras agregadas  esta consignada en 
    3GPP TSG RAN WG1 Meeting #92 R1-1801352 el cual es una reunion que se documento donde a groso modo generan una
    comparacion de como afecta la banda combinada a la velocidad real de transmision y no solo del factor de escala 
    sino de la ecuacion que TS 38.306 usa para su calculo de througthput, este mismo comentario se genera en 
    38.306 pero es necesario leer tsg RAn R1-1801352 Discussion on NR UE peak data rate para tener claridad.

    los valores para el factor de escala son  teniendo encuenta un
            1    para 1 cc
            0.8  para 2 cc
            0.75 para 2 cc + modulation
            0.4  para 3 cc + modulation

    el maximo de la modulacion a usar tambien es un factor relevante aunque nos dicen que para una sola frecuencia 
    portadora el factor de escala no inplica variaciones por el numero maximo del orden de modulacion, hacemos el 
    esfuerzo de documentarnos, y es mas de logica a la hora de la elavoracion de las simulaciones, contando como ejemplo lo 
    necesario para que un usuario en realidad se encuentre asignado su modulacion maxima debido a un componente de portadora
    o diferentes configuraciones, pero que no son apreciadas por el simulador al solo trabajar con un CC 
    """
    scaling_factor=[1,0.8,0.75,0.4]
    # El numero de bloques de recursos ya es tomado en otro modulo y explicado, aqui tomamos la cantidad de bloques de 
    # recursos tomados para un usuario 
    n_rb=n_rb_sistem
    # Los diferentes formatos para las ranuras TDD con OFDM  son consignados en TS 38.213 donde los formatos en la
    # Tabla 11.1.1-1: Slot formats for normal cyclic prefix  FORMAT 0 y FORMAT 4 o FORMAT 28 , sin usar simbolos flexibles
    #la razon por la cual no se escogen simbolos flexibles es en la parte de programacion, donde se mapea los bloques de
    # recursos asignados, si se usan simbolos flexibles, estos aportan interferencia tanto en el Downlink como en el 
    #Uplink ademas, como se hace la asignacion de canales tambien asignan de manera diferente los bloques de recursos
    # teniendo en cuenta las bandas de guarda, este simbolo flexible tiene dos formas diferentes de asignacion 
    """
        Programacion dinamica
                DCI en PDCCH
        Programacion semipersistente - el cual tiene 3 enfoques diferentes 
            proporciona al UE una configuracion para una celda especifica de un formato de slot (configuracion comun) 
            proporciona una configuracion dedicada para el uplink y control
            proporciona al UE unb formato para DCI
    """
    trama=10**(-3)/(14*2**numerologia)
    ## NOTA para esta configuracion el prefijo ciclico es asumido
    ##La cantidad de subportadoras OFDM es fija y es de 12 
    sub_ofdm=12
    # La cantidad de cabeceras por trama son calculadas dependiendo para que enlace se utilice la transmicion y la 
    # frecuencia portadora que esta utilice
    """
    Para el DL que es lo que nos interesa para el trabajo de grado los valores son 
            si Frp esta entre el rango de FR1
            0.14
            si Frp esta entre el rango de FR2
            0.18 
    """
    oh=[0.14,0.18]
    v_oh=(1-oh[1])
    throughput_user=n_cap_mimo*m_mod*scaling_factor*r_max*(n_rb*sub_ofdm/trama)*v_oh
    return throughput_user

def TBS_BLER(self,n_rb,n_ofdm,m_modulacion,v_mimo):
    n_dmrs=24
    n_oh=18
    r=asignar_r_max(m_modulacion)
    m_qam=m_modulacion
    n_rep=n_rb*n_ofdm-n_dmrs-n_oh
    n_re=min(156,n_rep)*n_rb
    n_info=n_re*r*m_qam*v_mimo
    if n_info <= 3824:
        n=max(3,math.floor(math.log2(n_info)-6))
        n_infop=max(24,2**n*math.floor(n_info/2**n))
    elif n_info >3824:
        n=math.floor(math.log2(n_info-24))-5
        n_infop=max(3840,(2**n)*round((n_info-24)/2**n))
    elif r <= 0.25:
        c= math.ceil((n_infop+24)/3816)
        tbs=8*c*math.ceil((n_infop+24)/(8*c))-24
    
    elif n_info > 8424:
        c=math.ceil(n_infop+24/3816)
        tbs=8*c*math.ceil((n_infop+24)/(8*c))
    else:
        tbs=8*math.ceil((n_infop+24/8))-24
    return tbs
def ber_sys(self,tbs):
    ber = 1- (1-0.1)**(1/tbs)
    return ber 

if __name__=="__main__":
	#Prototipo:
	#print("Modulacion")
    
    print("**************************************************")
    print("**********PRUEBA INTENAS modulaciones****************")
    print("**********desvanecimiento lento *******************")
    print("********** caso de uso eBMM**********************")
    print("**************************************************")
    
    orden_mqam=asignar_modulacion_mqam(3,'ebmm','lento')

    print('orden modulacion 16qam: ', orden_mqam)
    """
    print("**************************************************")
    print("********** PRUEBA INTENAS modulaciones****************")
    print("********** desvanecimiento lento *******************")
    print("********** caso de uso eBMM**********************")
    print("**************************************************")
    """
    orden_mqam=asignar_modulacion_mqam(9,'ebmm','lento')


    print('orden modulacion 64qam: ', orden_mqam)


    print("**************************************************")
    print("**********FIN pruebas MODULACION****************")
    print("**************************************************")

	#plan=Planificador(params_cfg, 17)
	#Planificador.asignar_100mhz()
	#REALIZAR PRUEBA DE F1,F2,F3
	#lista_rb()
	#prueba_asignar()
else:
	print("Modulo Importado: [", os.path.basename(__file__), "]")


    
    
    

