# epic-sns-5G: SAMI
Simulador a Nivel de Sistema 5G.

Para instalar, aceder mediante bash a la carpet: entorno_virtual_dependencias
Usar pip3 install --upgrade -r requirements_{fecha mas actual}.txt

### Instrucciones
El desarrollo de cada script debe seguir las siguientes fases: prototipo, pruebas y producción. 
Todos las variables deben ser llamados siguiendo el estilo PEP8 (Ver https://www.python.org/dev/peps/pep-0008/). Además el nombre de los scripts también deben seguir PEP8 y cada nombre debe corresponder con la carpeta donde se encuentra e.g., prot_nombre, prueb_nombre, prod_nombre.

#### Overview:
1. ANTES DE PROGRAMAR, REALIZAR PULL EN EL REPOSITORIO PARA ACTUALIZARO. Luego realizar commits periódicamente. Realizar PUSH solamente al terminar la jornada de programación.
2. Seguir el estilo PEP8 en variables, y nombres de script (teniendo en cuenta el protocolo anterior)
3. Todas las funciones, ¡TODAS! deben contener una breve explicación de que hace, y qué significa las variables internas.
4. Seguir la estructura de carpetas. 
5. Procurar agrupar scripts en una carpeta con un nombre que indique claramente su contenido.


#Prototipo (deprecated)
Se generan por primera vez los scripts, se desarrolla hasta que sus funcionalidades más básicas esten completas de acuerdo al plan de diseño inicial. Las pruebas de funcionalidad básica son inherentes al prototipo.

Cuando el prototipo esté completo:
1. Una vez terminado el script prototipo, copiar y pegar en la carpeta de pruebas cambiando el nombre como <<prueb_nombre>> y ensamblar con los demás scripts.

#Pruebas (deprecated)
Siguiendo la metodología iterativa, en este script se desarrollan e implmentan nuevas funcionalidades en el script, también se experimenta dichas funcionalidades y se ajusta el script de acuerdo al diseño y a las estructuras nuevas de datos o la arquitectura que pudo haber cambiando en el desarrollo del prototipo. Este script debe contener un plan de validación explicito en el método if__name__. Esta debe ser la fase más extensa, pues todas las funcionalidades deben estar completas y probadas. También debe ser explicito los comentarios.

## Sobre las ramas:
1: Crear RAMAS unicamente en esta carpeta, o de los scripts de esta carpeta. 

Cuando las pruebas son satisfactorias: 
1. Limpiar el código (borrar variables inncesarias, espacios innecesarios, comentarios innecearios)
2. Copiar y pegar en la carpeta de pruebas cambiando el nombre como <<prod_nombre>>.


### Producción
El script en producción es la versión final, por lo tanto no debe ser alterado. Ante un eventual cambio para corregir un bug, o adicionar funcionalidades, debe gestionarse mediante el flujo GIT unicamente. El repositorio siempre debe estar lo más organizado posible.

El script en producción:
1. El script no debe ser alterado en esta carpeta, solo en ramas y posteriomente integración por el lider del proyecto.

