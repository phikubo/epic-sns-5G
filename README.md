# Simulador a Nivel de Sistema 5G - SAMI


![uso1](https://user-images.githubusercontent.com/31525189/175200317-4015a753-c892-42eb-a0c3-c7353d2d91e0.png)

Requisitos:
1. Conexión a internet
2. Python 3.x instalado
3. Pip actualizado
  >>pip install --upgrade pip
4. (Opcional) Entorno virtual instalado y activo.

Para instalar, 
1. Descargar el simulador en GITHUB usando opción CODE>Download Zip.

  1.1 [OBLIGATORIO PARA UN DESARROLLADOR] Ejecutar un Fork, o solicitar colaboración al Desarrollador Lider.
  
  1.2 Copiar enlace HTTPS, inicializar el repositorio local y descargar el simulador, usando la terminal y GIT.
  >>git init
  >>git remote add origin https://github.com/phikubo/epic-sns-5G.git
  >>git pull origin master
  
2. Acceder mediante terminal a la carpeta: **entorno_virtual_dependencias**, y ejecutar:
>>pip install -r requirements.txt --upgrade

3. Ejecutar el script CONFIGURACION_INICIAL.py, para ello hacer doble click sobre el archivo y esperar que finalice. 

4. Acceder a la carpeta **produccion/sami_v1** y ejecutar:
>>python manage.py runserver

5. Operaciones GIT
*Nota: todos los cambios se deben realizar sobre una rama dev_*, la rama master se encuentra en producción y no debe cambiarse sin revisión.
  **Previo a cada cambio, actualizar la rama dev con los cambios mas recientes en master** [_en terminal o cmd_]:
  >>git pull origin master

  Para crear una nueva rama [_en terminal o cmd_]:
  >>git checkout -b dev_<nombre_desarrollador>
  
  Para guardar cambios localmente [_en terminal o cmd_]:
  >>git add .
  >>git commit -m "Descripcion del cambio"
  
  Para guardar cambios en rama del desarrollador [_en terminal o cmd_]:
  >>git push origin dev_<nombre_desarrollador>

  Para guardar cambios en rama de produccion [_EN GITHUB_]:
  1. Abrir un pull request con una breve descripción del cambio.
  2. Par revisor confirma que los cambios son efectivos y no alteran negativamente el funcionamiento del programa.
  3. Par revisor ejecuta un _MERGE_ y todos los cambios quedan guardados en master.

