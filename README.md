# epic-sns-5G: SAMI
Simulador a Nivel de Sistema 5G.

Para instalar, 

1. Acceder mediante terminal a la carpeta: **entorno_virtual_dependencias**, y ejecutar:
>>pip3 install -r requirements_<fecha>.txt --upgrade
  
2. Copiar todos los archivos de configuración del directorio **entorno_virtual_dependencias/configuracion_referencia/** al siguiente directorio **produccion/sami_v1.1/simapp/static/simulador/base_datos/**.
  
3. Acceder a la carpeta **produccion/sami_v1** y ejecutar:
>>python manage.py runserver
