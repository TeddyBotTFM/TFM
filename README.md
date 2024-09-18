# Grupo 6 de la Clase 2 del "Máster Data Science, Big Data & Business Analytics"

En esta rama del repositorio se muestran los códigos realizados para construir un sistema RAG, se ha dividido el código del proyecto en diferentes notebooks según el objetivo de cada una de las partes:
    
1) "CÓDIGO LIMPIEZA DE DATOS.ipynb": en este código se realiza la limpeza de la base de datos. No es necesario ejecutarlo para poder ejecutar el RAG, sin embargo, si se desea su ejecución se facilita la base de datos empleada en el código en la carpeta "DATOS" (también se deja a disposición el archivo .json con las contractions, archivo necesario para la ejecución del notebook)

2) "CÓDIGO GENERACIÓN BBDD VECTORIAL.ipynb": en este notebook se procede a la generación de la base de datos vectorial y a su posterior subida a Qdrant Cloud. No es necesaria su ejecución para el funcionamiento del RAG, ya que la base de datos se encuentra alojada actualmente en Qdrant Cloud (las credenciales de acceso a Qdrant se pueden obtener en el archivo .env facilitado junto con la memoria). Si se desea se puede realizar su ejecución, sin embargo, deben tener en cuenta que el resultado no será el mismo ya que las colecciones ya se encuentran almacenadas.

3) "CÓDIGO SISTEMA RAG.ipynb": este código muestra la creación del sistema RAG, es perfectamente ejecutable (únicamente serán necesarias las credenciales que se encuentran en el archivo .env facilitado junto con la memoria).

4) Carpeta de "SECURIZACIÓN", en esta carpeta se muestran las pruebas necesarias para obtener el System Message óptimo que más adelante se incorporará al notebook final del Sistema RAG. 

5) Carpeta de "FRONTEND", en esta carpeta se encuentra el código para el funcionamiento del sistema RAG en Whatsapp y Telegram, el código es perfectamente ejecutable y mantiene levantado el servidor en local, lo cual supone un problema si se quiere mantener levantado de manera indeterminada (se ofrece una solución a esta problemática en la memoria).