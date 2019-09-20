# epic-sns-5G
Simulador a Nivel de Sistema 5G.

## Instrucciones
El desarrollo de cada script debe seguir las siguientes fases: prototipo, pruebas y producción. 
Todos las variables deben ser llamados siguiendo el estilo PEP8 (Ver https://www.python.org/dev/peps/pep-0008/). Además el nombre de los scripts también deben seguir PEP8 y cada nombre debe corresponder con la carpeta donde se encuentra e.g., prot_nombre, prueb_nombre, prod_nombre.

Overview:
1. Seguir el estilo PEP8 en variables, y nombres de script (teniendo en cuenta el protocolo anterior)
2. Todas las funciones, ¡TODAS! deben contener una breve explicación de que hace, y qué significa las variables internas.


### Prototipo
Se generan por primera vez los scripts, se desarrolla hasta que sus funcionalidades más básicas esten completas de acuerdo al plan de diseño inicial. Las pruebas de funcionalidad básico son inherentes al prototipo.

Cuando el prototipo esté completo:
1. Una vez terminado el script prototipo, copiar y pegar en la carpeta de pruebas cambiando el nombre como <<prueb_nombre>>.


### Pruebas
Siguiendo la metodología iterativa, en este script se desarrollan e implmentan nuevas funcionalidades en el script, también se experimenta dichas funcionalidades y se ajusta el script de acuerdo al diseño y a las estructuras nuevas de datos o la arquitectura que pudo haber cambiando en el desarrollo del prototipo. Este script debe contener un plan de validación explicito en el método if__name__. Esta debe ser la fase más extensa, pues todas las funcionalidades deben estar completas y probadas. También debe ser explicito los comentarios.

Cuando las pruebas son satisfactorias: 
1. Limpiar el código (borrar variables inncesarias, espacios innecesarios, comentarios innecearios)
2. Copiar y pegar en la carpeta de pruebas cambiando el nombre como <<prod_nombre>>.


### Producción
El script en producción es la versión final, por lo tanto no debe ser alterado. Si un malfuncionamiento o bug se presenta, este debe ser editado en la carpeta de Pruebas y al terminar, debe ser remplazado en Producción, con el cambio de nombre correspondiente.

El script en producción:
1. El script no debe ser alterado en esta carpeta.
1.1 Si el script necesita cambios, editar el mismo script en Pruebas.
2. Copiar el script de producción y pegarlo en la carpeta Obsoleto.
3. Cuando el scrip de pruebas sea satisfactorio, reemplazar en Producción con el cambio de nombre. 
