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

  *Nota: todos los cambios se deben realizar sobre una rama dev_*, la rama master se encuentra en producción y no debe cabiarse sin revisión.
  Para crear una nueva rama:
  >>git checkout -b dev_<nombre_desarrollador>

2. Ejecutar el script CONFIGURACION_INICIAL.py, para ello hacer doble click sobre el archivo y esperar que finalice. 

3. Acceder a la carpeta **produccion/sami_v1** y ejecutar:
>>python manage.py runserver

