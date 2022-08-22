# mgh
<h2>Método del Gradiente Hidráulico</h2>
Implementación en python3 de la metodología de análisis de redes propuesta por Pilati y Todini, 1987 <br><br>

<h3>Objetivos</h3>
El objetivo de este sofware contar con una herramienta de docencia en los curso de hidráulica y mecánica de fluidos, y servir de base para modelos en tiempo real para toma desiciones a través de herramientas SCADA. <br>  No pretende ser un software poderoso y potente como EPANet, sino una herramienta liviana para integrar en SCRIPTS de python para usar con modelos diagramáticos y simples.  <br>Un objetivo adicional es podar contar con una herramienta para predecir desabastecimiento, a partir de datos en tiempo real.<br><br>

<h3>Descripción</h3>
En redacción <br><br>
El método se basa en que existe flujo permanente y se cumplen la conservación de energía en los nudos.<br>
<img src="f01.png"><br>
<h4>Características</h4>
<ol>
<li>Utiliza un archivo de entrada en formato CSV, pero se trabaja en el uso de un archivo JSON para hacer los datos más legibles
<li>Los resultados se obtienen por consola en un archivo tabulado, sin embargo se tiene pensado usar un archivo de salida en JSON
<li>Para el cálculo de las pérdidas por fricción se usa la ecuación de Darcy-Weisbach.  En el cálculo del factor de fricción f, se usa Swamee-Jain 
<li>Realiza la modelacición en forma puntual, un solo cálculo.  No se hace modelación en tiempo extendido.  No se modela el vaciado o llenado de tanques.
<li>El formato del archivo de entrada es tal cual sigue:
<pre>
Libro de Saldariaga                           TITULO
Ing. Carlos Camacho                           AUTOR
28/01/2019                                    FECHA
V0.01                                         VERSION
1.141E-6,1.0E-5,40                            VISCOSIDAD DINÁMICA, TOLERANCIA, ITERACIONES
1,5,7,1                                       NUDOS DE CARGA, NUDOS DE DEMANDA, TRAMOS, FACTOR DE DEMANDA GLOBAL
0,100,110,*                                   NUDO DE CARGA: NUMERO, ELEVACIÓN, CARGA, DEMANDA 
1,  90,  60,1                                 NUDO DE DEMANDA: NUMERO, ELEVACIÓN, DEMANDA, FACTOR
2,  90,  -40,1                                NUDO DE DEMANDA: NUMERO, ELEVACIÓN, DEMANDA, FACTOR 
3,  90,  30,1                                 NUDO DE DEMANDA: NUMERO, ELEVACIÓN, DEMANDA, FACTOR
4,  90,  30,1                                 NUDO DE DEMANDA: NUMERO, ELEVACIÓN, DEMANDA, FACTOR
5,  90,  40,1                                 NUDO DE DEMANDA: NUMERO, ELEVACIÓN, DEMANDA, FACTOR
0,  0,  1,  500,  250,  0.0015,  0,  TA, -    TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
1,  1,  2,  400,  150,  0.0015,  10,  TA, -   TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
2,  3,  2,  200,  100,  0.0015,  0,  TA, -    TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
3,  4,  3,  400,  150,  0.0015,  0,  TA, -    TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
4,  1,  4,  200,  100,  0.0015,  0,  TA, -    TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
5,  5,  4,  600,  200,  0.0015,  0,  TA, -    TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
6,  0,  5,  300,  250,  0.0015,  0,  TA, -    TRAMO: NUMERO, DESDE, HASTA, LONGITUD, DIAMETRO, Ks, KL, TIPO, OPCIONES
</pre>

<li>Tipos de nudo: <ul>
  <li> NC: Nudos de carga. Representan tanques o embalses. Actualmente son indiferentes porque no hay corridas de tiempo extendido.
     Los datos requeridos son: número de nudo, elevación [m], carga [m], tipo (T o E) el tipo no está implementado
  <li>ND: Nudos de demanda. Representan puntos de la red donde hay consumo y por lo tanto pre4sión dependiente de la demanda
     Los datos requeridos son: número de nudo, elevación [m], demanda [l/s], factor de demanda
  </ul>
<li>Tipos de tramo: <ul>
  <li>Tramo de tubería: Representan un tramo normal de tubo que puede estar cerrado o abierto.
     Los datos requeridos son: número de tramo, Desde y Hasta (topología de red), Longitud [m], Diámetro [mm], Ks [mm], KL, Estado TA= Tubería Abierta
     TC= Tubería Cerrada, Opciones (no tiene)
  <li>Válvula de control: Puede ser una válvula reductora de presión VR o una válvula sostenedora de presión VS.
     Los datos requeridos son: número de tramo, Desde y Hasta, Longitud de la cachera [m], Diámetro [mm], Ks [mm], KL, Tipo VS= Válvula Sostenedora
     VR= Válvula Reductora, Consigna [m] 
  <li>Bomba en un tramo de tubería: Los datos requeridos son: número de tramo, Desde y Hasta, Longitud de la cachera [m], Diámetro [mm], Ks [mm], KL,
     BO = Bomba, Coeficientes de la curva: alfa, beta, gama
  </ul>
<li>Tipos de corrida:<ul>
  <li>quiet o silencioso: muestra únicamente los valores de las tablas de cargas en los nodos y los caudales en los tramos de la última iteración 
  <li>normal: muestra las tablas de nudos y de tramos para la última iteración 
  <li>detallado (verbose): muestra las matrices del modelo, y las tablas de los datos de nudos y tramos de cada iteración
  </ul></ol>

<h4>Estado Actual</h4>

<h4>Por desarrollar</h4>
<ol>
  <li>Se debe desarrollar una interfaz de usuario para construir cada modelo, y hacer los archivos de entrada.
  <li>Se debe trabajar en el desarrollo de un tramo tipo "Válvula de retención o Check"
  <li>Emisores en los nudos de demanda
  <li>Ajuste de presiones negativas.  Es realmente importante qu el sistema se reponga del error de obtener presiones negativas cuando
    las consideraciones de demanda lo llevan más allá de las posibilidades físicas de caudal y carga.  Debe hacerse un algoritmo que iniciando con los 
    nudos negativos ajuste los caudales de demanda para que la presión en los nodos no tenga valores negativos en ninguna parte de la red.  Esto implica 
    que existirán lugares con demanda cero a causa del incremento de la demanda en otros nudos, empezando a afectar de arriba a abajo. 
    <li>Modelar en tiempo extendido, para considerar vaciado/llenado de tanques. Es necesario cambiar el archivo de entrada para incluir área de tanque y altura máxima
  </ol>
  
 
  
Carlos Camacho Soto, 2022
