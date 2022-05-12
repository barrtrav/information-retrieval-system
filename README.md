# information-retrieval-system
Projecto de SRI 5to Ciencia de la Computación
Autor: Reinaldo Barrera Travieso - C511

Actualmente el proyecto se encuentra en desarrollo, por lo que a continuacion se 
enumerara lo que se tiene escho hasta el momento y despues lo que se espera tener para el final

## Realizado:

El proyecto se basa en un sistema de recuepracion de infomracion usando uno de los modelos clasico 
dados en el curso, en este caso el modelo vectorial. Para esto se modelan los siguientes objectos o clases:

* Docuemnt: Es la estructura que almacena los documentos. Esta esta formada por el id del docuemento, el titulo, 
una lista de lexer que representa los terminos del documentos ya procesados y el texto original.

* Token: Es la estructura que almacena los terminos. Esta esta formada por un lexer que representa el termino, un diccionario de docuemtnos vs frecuencia del termino en el y un entero que almacena la maxima frecuencia deltermino.

* TokenList: Esta estuctura almacena una lista de tokens en fomra de diccionario para realizar el mapeo.

* Corpus: Los corpus son estructuras que representan los data set o colleccion de documentos. Este posee una lista de docuemntos, y un tokemlist con todos los token existentes.

* Model: Esta estructura es la que representa el modelo vectorial y realiza la operaciones de similitud y ranking.

* System: Este almacena un modelo.

Hasta el momento al ejecutar el proyecto te carga el set de datos y te pide un query o consulta y te devuelve una lista de id de los documentos recueprados. Para faciliatr la carga se emplea una base de datos en sqlite3, si se ejecuta por primera vez esta base de datos es creada y las restante veces solo carga los datos de esta. Por tanto es necesario tener instalada en la pc sqlite3

El proyecto pose una app desarrollada en django para la parte visual que toma la base de datos y te procesa las consultas. No obtsante esta base de datos debe existir ya en la maquina por lo que se debe primero ejecutar el projecto sin la parte visual. No obstante en la entrega final se pretende integrar en un script esta funcion conjunta.

Para ejecutar el proyecto se tiene dos vias:

```bash
$cd src
$python3 main.py
```
Esto carga el projecto en consola

```bash
$cd src
$bash runserver.sh
```
Esto levanta un servidor en django por lo que despues de ejecutar el comando se debe entrar al url="127.0.0.1:8000/index" para la parte visual

## Sin hacer

* Incorporar los parse de los demas dataset

* Implementar los codigo para realizar los test

* Feedback

* Retroalimentacion

* Expansión de consultas

* Integración con algoritmos de Crawling

* Recomendacion de documentos

* Realizar el informe o reporte

* Ortografia de este documento
