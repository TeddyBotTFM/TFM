# Grupo 6 de la Clase 2 del "Máster Data Science, Big Data & Business Analytics"

Este TFM busca obtener un sistema RAG que conteste preguntas relacionadas únicamente con la motivación. 

Se compone de diferentes códigos, algunos de ellos no es necesario ejectuarlos, se especifica mediante mensaje aquellos códigos que no es necesario ejectuar: 
    
1) "CÓDIGO GENERACIÓN BBDD VECTORIAL.ipynb" y "CÓDIG LIMPIEZA DE DATOS.ipynb" no es necesario ejecutarlos debido a que su utilidad es la creación de la base de datos vectorial, esta se encuentra actualmente accesible en Qdrant Cloud (se proporcionan credenciales en un archivo .env facilitado junto con la memoria)
    
2) Carpeta de "SECURIZACIÓN", en esta carpeta se muestran las pruebas necesarias para obtener el System Message óptimo que más adelante se incorporará al notebook final del Sistema RAG. 

3) Carpeta de "FRONTEND", en esta carpeta se encuentra el código para el funcionamiento del sistema RAG en Whatsapp y Telegram, sin embargo, al encontrarse en un servidor local este solo puede ser ejecutado si el dispositivo se encuentra activo (en la memoria se establece una solución a esta problemática)