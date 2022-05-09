# epic-sns-5G: SAMI
Simulador a Nivel de Sistema 5G.


Requisitos:
1. Conexión a internet
2. Python 3.x instalado
3. Pip actualizado
  >>pip install --upgrade pip
4. (Opcional) Entorno virtual instalado y activo.

Para instalar, 

1. Acceder mediante terminal a la carpeta: **entorno_virtual_dependencias**, y ejecutar:
>>pip install -r requirements.txt --upgrade

  *Nota: provisionalmente hacer un cambio a la rama fusion-master, la rama master se encuentra en desarrollo para su depuracion de bugs*
  >>git checkout fusion-master

2. Copiar todos los archivos de configuración del directorio **entorno_virtual_dependencias/configuracion_referencia/** al siguiente directorio **produccion/sami_v1.1/simapp/static/simulador/base_datos/**. Nota: La carpeta "escenarios" en la direccion de destino se remplaza completamente. 

3. Acceder a la carpeta **produccion/sami_v1** y ejecutar:
>>python manage.py runserver

