from django.urls import path
from . import views 

app_name='simapp'
urlpatterns = [
    #http://127.0.0.1:8000/ / 
    path('', views.home, name='presentacion_v1'),
    #
    path('sim/', views.form_a1, name='sim_form_a1'),
    path('sim/form_a2', views.form_a2, name='sim_form_a2'),
    path('sim/form_a3', views.form_a3, name='sim_form_a3'),
    path('sim/form_a4', views.form_a4, name='sim_form_a4'),
    #
    path('sim/form_compacto', views.form_compacto, name='sim_form_compacto'),
    #
    path('sim/parametros/', views.ver_parametros, name='parametros'),
    #simulador
    path('sim/iniciar/', views.iniciar_simulacion, name='iniciar_sim'),
    #
    path('sim/simulacion-general', views.ver_presim, name='pre_sim'),
    path('sim/simulacion', views.ver_sim, name='sim'),
    #path('simulador/tablas', views.ver_tablas, name='simulador_tablas'),
    #path('simulador/logs', views.ver_tablas, name='simulador_tablas'),

    #auxiliar
    path('demo_sami_v1/', views.form_demo_sami_v1, name='demo_form_sami_v1'),
    path('futuro/', views.futuro, name='futuro'),


]