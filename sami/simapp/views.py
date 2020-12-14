from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'simapp/sami-index.html')

def formulario_sami_v1(request):
    return render(request,'simapp/form-wizard.html')

def en_desarrollo(request):
    return render(request,'simapp/sami-en-desarrollo.html')

#def test_sam(request):
#    return render(request,'simapp/sami-index.html')