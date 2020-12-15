from django.urls import path
from . import views 
from .forms import FormStepOne, FormStepTwo
from .views import FormWizardView


app_name='simapp'
urlpatterns = [
    #http://127.0.0.1:8000/ / 
    path('', views.home, name='caracteristicas'),
    path('sami_v1/', views.form_demo_sami_v1, name='demo_form_sami_v1'),
    path('futuro/', views.en_desarrollo, name='futuro'),
    path('test/', FormWizardView.as_view([FormStepOne, FormStepTwo]), name='dev_sami'),
    

]