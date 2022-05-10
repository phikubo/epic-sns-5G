from django.urls import path
from . import views 

app_name='simapp'
urlpatterns = [
    #http://127.0.0.1:8000/ / 
    path('', views.home, name='presentacion_v1'),
    #
    #no se usan los formularios de fases, a pesar de que se pueda accesar a las rutas, no es posible guardar los parametros.
    #path('sim/', views.form_a1, name='sim_form_a1'),
    #path('sim/form_a2', views.form_a2, name='sim_form_a2'),
    #path('sim/form_a3', views.form_a3, name='sim_form_a3'),
    #path('sim/form_a4', views.form_a4, name='sim_form_a4'),
    #
    path('simulador/parametros', views.ver_parametros, name='lista_parametros'),
    #
    path('simulador/seleccionar_escenario', views.seleccionar_escenario, name="sim_form_escenarios"),
    #
    path('simulador/form_compacto', views.form_compacto, name='sim_form_compacto'),
    #
    #SI TIENE REDIRECT, DEBE TERMINAR EN /, DE LO CONTRARIO NO ES NECESARIO.
    #@redirect
    path('simulador/ejecutar_parametros/', views.ejecutar_parametros, name='parametros'),
    #simulador
    path('simulador/iniciar', views.iniciar_simulacion, name='iniciar_sim'),
    #
    path('resultados/simulacion-general', views.ver_presim, name='pre_sim'),
    path('resultados/simulacion', views.ver_sim, name='sim'),
    
    #path('simulador/tablas', views.ver_tablas, name='simulador_tablas'),
    #path('simulador/logs', views.ver_tablas, name='simulador_tablas'),
    path('estadisticas/seleccionar_comparacion', views.seleccionar_comparacion, name="sim_form_comparar_escenarios"),
    #@redirect
    path('estadisticas/resultados_comparacion/', views.resultados_comparacion, name="sim_resultados_comparacion_escenarios"),

    #auxiliar
    #path('extra/demo_sami_v1/', views.form_demo_sami_v1, name='demo_form_sami_v1'),
    path('extra/futuro/', views.futuro, name='futuro'),


]