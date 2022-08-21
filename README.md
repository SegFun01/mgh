# mgh
Método del Gradiente Hidráulico
Implementación en python3 de la metodología de análisis de redes propuesta por Pilati y Todini, 1987

Modelos hidráulicos en redes de tuberías

Características
1. Utiliza un archivo de entrada en formato CSV, pero se trabaja en el uso de un archivo JSON para hacer los datos más legibles

2. Los resultados se obtienen por consola en un archivo tabulado, sin embargo se tiene pensado usar un archivo de salida en JSON

3. El formato del archivo de entrada es tal cual sigue:
---
<p>
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
<p>

4. Tipos de nudo: 
  a) NC: Nudos de carga. Representan tanques o embalses. Actualmente son indiferentes porque no hay corridas de tiempo extendido
     Los datos requeridos son: número de nudo, elevación [m], carga [m], tipo (T o E) el tipo no está implementado
  b) ND: Nudos de demanda. Representan puntos de la red donde hay consumo y por lo tanto pre4sión dependiente de la demanda
     Los datos requeridos son: número de nudo, elevación [m], demanda [l/s], factor de demanda

5. Tipos de tramo:
  a) Tramo de tubería: Representan un tramo normal de tubo que puede estar cerrado o abierto.
     Los datos requeridos son: número de tramo, Desde y Hasta (topología de red), Longitud [m], Diámetro [mm], Ks [mm], KL, Estado TA= Tubería Abierta
     TC= Tubería Cerrada, Opciones (no tiene)
  b) Válvula de control: Puede ser una válvula reductora de presión VR o una válvula sostenedora de presión VS.
     Los datos requeridos son: número de tramo, Desde y Hasta, Longitud de la cachera [m], Diámetro [mm], Ks [mm], KL, Tipo VS= Válvula Sostenedora
     VR= Válvula Reductora, Consigna [m]
  c) Bomba en un tramo de tubería: Los datos requeridos son: número de tramo, Desde y Hasta, Longitud de la cachera [m], Diámetro [mm], Ks [mm], KL,
     BO = Bomba, Coeficientes de la curva: alfa, beta, gama
     
6. Tipos de corrida:
  a) quiet o silencioso: muestra únicamente los valores de las tablas de cargas en los nodos y los caudales en los tramos de la última iteración
  b) normal: muestra las tablas de nudos y de tramos para la última iteración
  c) detallado (verbose): muestra las matrices del modelo, y las tablas de los datos de nudos y tramos de cada iteración

Estado Actual

Por desarrollar
1. Se debe desarrollar una interfaz de usuario para conbstruir cada modelo, y hacer los archivos de entrada.

Carlos Camacho Soto, 2022
