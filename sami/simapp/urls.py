from django.urls import path
from . import views


app_name='simapp'
urlpatterns = [
    #http://127.0.0.1:8000/ / 
    path('', views.home, name='caracteristicas'),
    path('sami_v1/', views.formulario_sami_v1, name='form_sami_v1'),
    path('futuro/', views.en_desarrollo, name='futuro'),
    #path('test/', views.test_sam, name='test'),
    

]