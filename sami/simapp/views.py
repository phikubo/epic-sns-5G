from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'simapp/index.html')

def formulario_sami_v1(request):
    return render(request,'simapp/form-wizard.html')