from django.urls import path
from . import views 
from .forms import FormStepOne, FormStepTwo
from .forms import FormGeneral
from .views import FormWizardView


app_name='simapp'
urlpatterns = [
    #http://127.0.0.1:8000/ / 
    path('', views.home, name='caracteristicas'),
    #simulador
    path('sim/iniciar/', views.iniciar_simulacion, name='iniciar_sim'),
    #
    path('sim/', views.form_a1, name='sim_form_a1'),
    path('sim/form_a2', views.form_a2, name='sim_form_a2'),
    path('sim/form_a3', views.form_a3, name='sim_form_a3'),
    path('sim/form_a4', views.form_a4, name='sim_form_a4'),
    #
    path('sim/estadisticas', views.ver_estadisticas, name='simulador_estadisticas'),
    #path('simulador/tablas', views.ver_tablas, name='simulador_tablas'),
    #path('simulador/logs', views.ver_tablas, name='simulador_tablas'),

    #auxiliar
    path('demo_sami_v1/', views.form_demo_sami_v1, name='demo_form_sami_v1'),
    path('futuro/', views.en_desarrollo, name='futuro'),
    
    #test
    path('test_wizzard/', FormWizardView.as_view([FormStepOne, FormStepTwo]), name='dev_sami'),
    path('test2/', views.form_view_2, name='dev_sami_2'),
    

]