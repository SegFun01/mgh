
# WIP: Work in progress
Carlos Camacho Soto <br>
Método del Gradiente Hidráulico<br>
2022<br><br>

## Notas sobre los pendientes de desarrollo de MGH
### Nombres de nudo y tramo
Se requiere incluir en los archivos de la red además del identificador de nudo y de tramo un nombre en forma de un código para relacionar cada elemento con su correspondiente en la vida real.   Para el modelo es necesario nombrar a los nudos con un identificador [id] de tipo integer, contando desde 0, porque se debe acceder a la posición de cada elemento en una matriz de 1 o 2 dimensiones.   Con ese [id] relacionado con un [nombre] se puede leer el archivo de entrada y salida con un formato más apto para los humanos (human readable)
Ejemplos:
    
       “nombre”: TQ01-M01-Curridabat
       “nombre”: VR01-M01-Tinoco01


### Lista de tipos de elementos
Elementos tipo nudo
Los elementos tipo nudo asignan el nivel topográfico de las tuberías y los puntos de demanda. Son requeridos como puntos de conexión entre los tramos de tubería. Todos los nudos a excepción de los nudos de carga pueden tener asignado un valor de caudal demandado.
A los nudos de carga fija se les calcula un valor de “Caudal recibido o aportado” con el cual calcular el ∆H en el nivel de tanque entre cada iteración de tiempo extendido.
| Símbolo | Tipo     | Descripción | Parámetros extra |
|---------|----------|-------------|------------------|
|NC       |Carga fija|Tanque o embalse |  V, H      |
|NE       |Emisor|Hidrante, aspersor, fuga|Ecuación|
|NF|Fuente|Producción fija|-q, curva FVP|
|ND|Demanda|Nudo de demanda|+q, curva FVH|

## Elementos tipo línea
Todos los elementos tipo línea son modelados como tubería, es decir cuentan con características de longitud, diámetro, coeficientes de pérdidas, de modo que el funcionamiento de bomba, válvula, etc es adicional a su comportamiento como tubo simple, es decir que el tramo donde se ubique una válvula o bomba tendrá pérdidas de carga asociadas a su longitud, diámetro y coeficientes de pérdidas.
|Símbolo|Tipo|Descripción|Parámetros extra|
|-------|----|-----------|----------------|
|TB|Tubería|Tubería cimple abierta o cerrada|Estado: 0, 1|
|VR|Reductora|Válvula reductora de presión|Consigna|
|VS|Sostenedora|Válvula sostenedora de presión|Consigna|
|CK|Check|Válvula de retención o check|-|
|VQ|Caudal|Válvula reguladora de caudal|q
|BO|Bomba|Equipo de bombeo en línea|α, β, γ|
|VB|Boya/Altitud|Válvula de boya y válvula de altitud|Consigna (H/P)|

## Reposición de estado de presiones negativas
Cuando existan presiones negativas en la red, en los nodos con carga negativa, el caudal asignado es incongruente con la presión negativa.  Entonces el caudal debe ser menor, pero no se sabe cuánto.  La propuesta de algoritmo es buscar el nudo con la presión más negativa, y reducir la demanda del nodo un valor ∆q, proporcional a la demanda qi (por ejemplo ∆q =qi*0.1), de manera que el nuevo q sea: qi+1 = 0.9*qi.   
Con esa nueva demanda en el nudo se vuelve a correr la red.  En esta nueva corrida necesariamente variarán las presiones en general de la red, deben ser mayores, por lo que uno o varios nudos que tenían carga negativa deben llegar a cargas positivas.   
Si siguen existiendo presiones negativas, vuelve a seleccionar el nudo de la mínima presión y vuelve a ajustar el caudal demandado factorizándolo de la manera explicada anteriormente: qi+1 = 0.9*qi.   
Se prosigue en ese procedimiento de ajuste de demandas hasta que no haya nudos con presión negativa o hasta que el caudal de dichos nodos afectados sea cero.   
Aquellos nudos que lleguen a demanda cero qi=0 serán consistentes con “desabastecimiento” espontáneo, es decir no causado por un cierre de tuberías por mantenimiento o falla.
En el proceso, el archivo de entrada va a sufrir una variación para que el modelo realice dicha reposición; por lo tanto, es necesario que en este proceso de reposición, el archivo de entrada y salida iniciales sean guardados intactos y se construya un nuevo archivo con las iteraciones de los nuevos datos de entrada y salidas.   
Este proceso no debe ser automático, sino que debe ser solicitado por el usuario, ya que dependiendo de las necesidades puede ser requerido no hacerlo.   
Se propone que se pueda ejecutar esta rutina de reposición por medio de un modo de ejecución:
    
     # python3 mgh.py archivo_red.mgh -r
-r   modo de ejecución con rutina de reposición por presiones negativas.   

Este modo de ejecución arroja los resultados de la corrida normal, pero finalmente arroja un archivo adicional con las demandas y presiones reales máximas posibles y el estado de caudales en los tramos, que permiten tener una estimación de los niveles de desabastecimiento y/o reducción de la satisfacción de la demanda en cada nudo

## Modos de ejecución
Algunos de los modos de ejecución y formatos de archivo propuestos para el programa ya han sido implementados, sin embargo, se requieren nuevos modos de ejecución y combinaciones de ellos.  A continuación una lista de los modos propuestos:
|Modo|Uso|Estado|
|----|----|------|
|-v|Detallado: imprime los datos de iteraciones, matrices y Resultados|OK|
|-q|Callado: solo muestra vectores de Q, H y P|OK|
|-n|Normal: imprime tabla de datos y resultados de nudos y tramos|OK    
|-m|Mute: no envía datos ni salida a stdout ni stderr, solo a file|WIP|
|-i|Interactivo: permite pasar los datos de la red por terminal input|OK|
|-r|Reposición: Reponerse de presiones negativas en nudos|WIP|
|-j|JSON: salida de datos en forma de json.  Función de API|WIP|
|-t|TXT: salida de información en formato txt en tablas|WIP|
|-c|CSV: salida de información en formato csv para importar en EXCEL|WIP|
|-f|file: envía la salida a un archivo|WIP|
|-x|Extendido: ejecución en tiempo extendido, en pasos de 1 hora|Previsto|

### Comentarios acerca de los modos, y como deberán quedar trabajando:
- El modo -f duplica/redirige la salida al archivo fout, según el formato requerido, puede ser usado en combinación con todos los modos: -m, -q, -n, -v y los formatos -t, -j, -c
- el modo -q por defecto envía a la terminal las matrices Q, H, P y qi en forma de tablas.  Combinando con -c, -t, -j se puede definir el formato de salida requerido: CSV, TXT, JSON.
- El modo -v envía una salida detallada a stdout en forma de TXT.  En combinación con -f, envía la salida detallada al archivo stdout en formato TXT.  Si se combina con -c ó -j, envía solamente el reporte final (el mismo que envía -n), de acuerdo con el formato indicado c: CSV, j: JSON
- El modo de salida -m, no envía ninguna salida a stdout.  Puede ser usado en combinación con -n y -j, -t ó -c para enviar al archivo de salida fout de acuerdo al formato requerido.  También puede ser usado en combinación con -q para enviar solamente los datos de Q, H, P y qi directamente a archivo sin enviar a terminal.

Se listan algunas combinaciones de modos y formatos:
|Opción|Resultado|
|------|---------|
|-q -qj -qc|Salida de Q, H, P y qi en formato TXT/JSON/CSV hacia stdout|
|-qf -qjf -qcf|Salida de Q, H, P y qi en formato TXT/JSON/CSV hacia archivo|
|-n -nj -nc|Reporte normal en formato TXT/JSON/CSV hacia stdout|
|-nf -njf -ncf|Reporte normal en formato TXT/JSON/CSV hacia archivo|
|-v |Informe detallado en formato TXT hacia terminal stdout|
|-vf |Informe detallado en formato TXT hacia archivo|
|-vjf -vcf|Informe detallado en formato JSON/CSV hacia |archivo ***
|(null)|La salida por defecto es -n|


*** este tipo de salida puede no ser significativo ó util: omitir.

##Separar archivos de entrada de datos
Los datos de entrada del modelo de una red se compones de al menos 2 partes principales:
- Datos topológicos de la red 
- Parámetros hidráulicos que serán usados en la simulación
- Datos de configuración generales
A la hora de crear un “proyecto” se crearán estos 3 documentos:
- `nombre_proyecto.tpl.json`   topología de la reducción
- `nombre_proyecto.prm.json`  parámetros de la ejecución
- `nombre_proyecto.pat.json`  patrones de demanda/producción
- 
Es conveniente separar los datos de entrada según sus componentes en varios archivos independientes.   
Uno (`nombre_proyecto.prm.json`) contendrá los parámetros de estado de la red tales como niveles de tanque, demandas, con sus respectivas fecha y hora y junto con los patrones o curvas de demanda, en un archivo de entrada independiente, de modo que pueda ser construido con datos de un SCADA, digitados o por medio de un módulo API, para hacer corridas con diferentes escenarios en una red existente.  Los datos que se incluirían en este archivo serían:
### Tipo de elemento
Parámetros a incluir en archivo de entrada
Nudos de carga fija
[id] [carga, fecha, hora]
Nudos de demanda
[id] [demanda, fecha, hora] [curva de demanda]
Nudos tipo naciente
[id] [producción, fecha, hora] [curva de producción]
Nudos tipo emisor
[id] [ecuación] [estado, fecha hora]
Tramos simples
[id] [estado, fecha, hora]
Tramos tipo válvula
[id] [consigna, fecha, hora]
Tramos tipo bomba o booster
[id] [estado, fecha,hora] [opciones, fecha, hora]

El otro archivo (`nombre_proyecto.tpl.json`) contendrá los valores intrínsecos de la topología, tales como: 
    • Nudos: identificador, tipo, cota topográfica y nombre
    • Tramos: desde, hasta, L, D, ks, kL, tipo
Actualmente el tipo de tramo se escoge en el campo de [Estado] porque inicialmente se pensó en que una tubería podía estar abierta o cerrada, podía tener estado=TA (tubería abierta) y estado=TC (tubería cerrada).  Sin embargo al aparecer otros tipos de tubería, el [estado] se debe cambiar por [tipo] y en caso de requerir que la tubería esté abierta o cerrada se debe indicar en una nueva variable de [estado] con valores 0=cerrada y 1=abierta, ya que todos los elementos tipo línea funcionan como una tubería simple y además pueden tener sobrepuesto el funcionamiento tipo accesorio. Esto se muestra en los siguientes ejemplos.
Registro actual para tubería simple
{
"id": 0,
"desde": 0,
"hasta": 1,
"longitud": 100.0,
"diametro": 300.0,
"ks": 0.05,
"kL": 0.0,
"estado": "TA",
"opciones": "-"
}
Registro para tubería simple
{
"id": 0,
"desde": 0,
"hasta": 1,
"longitud": 100.0,
"diametro": 300.0,
"ks": 0.05,
"kL": 0.0,
"tipo": "TB",
"opciones": "-",
“estado”: 1   (0=cerrada, 1=abierta)
}

Registro actual para Bomba
{
"id": 9,
"desde": 2,
"hasta": 5,
"longitud": 100.0,
"diametro": 150.0,
"ks": 0.05,
"kL": 2.0,
"estado": "BO",
"opciones": "-3125.0 187.5 77.5"
}

Registro para Bomba propuesto
{
"id": 9,
"desde": 2,
"hasta": 5,
"longitud": 100.0,
"diametro": 150.0,
"ks": 0.05,
"kL": 2.0,
"tipo": "BO",
"opciones": "-3125.0 187.5 77.5",
“estado”: 1
}

Registro actual para Reductora
{
"id": 4,
"desde": 3,
"hasta": 4,
"longitud": 1000.0,
"diametro": 150.0,
"ks": 0.05,
"kL": 2.0,
"estado": "VR",
"opciones": "10"
}

Registro para Reductora propuesto
{
"id": 4,
"desde": 3,
"hasta": 4,
"longitud": 1000.0,
"diametro": 150.0,
"ks": 0.05,
"kL": 2.0,
"tipo": "VR",
"opciones": "10",
“estado”: 1
}


Tubería en canal abierto
Una idea que puede ser útil para modelar sistemas deficitarios consiste en determinar si una tubería ingresa a régimen de canal abierto, en cuyo caso, la ecuación de tubos a presión ya no es válida, y tampoco lo será el caudal transportado por la tubería, de modo que se afectan las posibles demandas de los nodos que dependen de dicho tramo.
Se requiere trabajar en un algoritmo que pueda cambiar entre tubo a presión y tubo a canal abierto en dichos casos.
Consideraciones sobre tuberías a régimen de canal abierto:
    • Una tubería puede ir a canal abierto siempre que la pendiente del tramo permita tener una velocidad a canal abierto superior a la velocidad de flujo a presión.  Esto es cuando el caudal del tramo de acuerdo a la compensación de caudales de la red sea inferior al caudal máximo posible a canal abierto.
    • Debe cumplirse además que la presión en el nodo de inicio del tramo debe ser igual a cero, lo que implica entrada de aire en la tubería a través del nodo que en lugar de aportar la demanda requerida.
    • Es necesario asignar a los tubos un valor para la “n” de manning con el cual analizar la capacidad a canal abierto de cada tramo de tubería.
    • Se debe analizar cómo se analizan los tramos con pendiente inversa y los sifones.  En vista de la forma de construir el modelo no se pueden modelar sifones sin la ayuda de nudos intermedios.
    • Si el nudo de llegada tiene una presión negativa, se asume que en el nodo no hay aporte de caudal, sin embargo en la realidad las acometidas están distribuidas a lo largo de la tubería, podría usarse ena regla de proporcionalidad para determinar que porcentaje de la demanda es insatisfecha, estimando un nivel a lo largo de la tubería tubería tiene pendiente inversa. La distancia x de la siguiente ecuación sería la proporción de tubo seco.





Vaciado de tanques 
Si bien es cierto, lo usual en modelos hidráulicos es que al llegar a nivel de tanque mínimo, el nudo correspondiente “se desconecta” con lo que el nivel no “baja por la red”. En la realidad los niveles de tanque pueden ser negativos, e ir más abajo del nivel de piso, descendiendo por la tubería a medida que se va vaciando la red.  Con el fin de simular esta situación y que el modelo pueda predecir en qué momento el tanque va a iniciar verdaderamente el llenado, el cual ocurre luego de que termina de rellenarse la red, se propone que en el modo de ejecución extendido se permita al nivel de los nudos de carga que puedan adoptar valores negativos,.  Lo mismo se permitirá hacia el lado del nivel máximo, pudiendo permitir estimar un volumen rebalsado y un tiempo de rebalse.
El hecho de desconectar el tanque, o el de cerrar o abrir válvulas de entrada y salida permite evitar estos escenarios.

Tubería cerrada
TC
Válvula de retención (check)
CK
Ejecución en tiempo extendido
Para la ejecución en tiempo extendido es necesario definir:
    • La hora de inicio de la ejecución, es decir a que hora corresponden los niveles de tanque, y a que hora asignar los valores de la curva de demanda y produccion
    • La cantidad de unidades de tiempo (horas) para las que se realizará la corrida
    • Se define que estas unidades de tiempo corresponden a horas, no se prevé que sea necesario que esto cambie.
    • Deben estar definidas las curvas correspondientes y asignadas a los nudos, ya sea producciones o demandas
    • Definir vectores de salida para Q, H, Ho, P, qi, en los cuales se registren los valores de los resultados de cada hora.  Pueden llamarse Qx, Hx, Hox, Px, qix.  En los reportes de salida se itera n veces de acuerdo a la duración.
    • En el archivo *.prm.json se debe consignar la duración del tiempo extendido.  Si duración es 0 se ejectua en modo simple, y se utilizan los valores de factor_global y factores de cada nudo.  Si la duración >0, se usan los patrones definidos en cada nudo.

Curvas de variación de caudal
Las curvas de variación de caudales, ya seas curvas de variación de la demanda o curvas de variación de producción.  Se proponen los siguientes:
a. Curva de variación horaria: contendrá 24 tuplas de [“hora”: fhv], iniciando a las 0 horas, por ejemplo:
"fvh":[{"0": 0.53, "1":0.56,  "2":0.59,  "3":0.62,  "4":0.66,  "5":0.74, "6":1.06,  "7":1.38,  "8":1.53,   "9":1.68, "10":1.48, "11":1.29, "12":1.21, "13":1.14, "14":1.11, "15":1.09, "16":1.07, "17":1.04,  "18":1.01, "19":0.99, "20":0.94, "21":0.89, "22":0.76, "23":0.63}]
Estas curvas pueden ser varias, y se pueden asignar independientementa a cada nudo.  Es ideal tener al menos una curva de demanda domiciliar, y curvas comerciales, industriales, educativas/gobierno, ya que estos diferentes usos pueden tener diferentes comportamientos.
b. Curva de variación por día de la semana: en algunos escenarios el comportamiento de los usuarios a lo largo de la semana es diferente, especialmente los fines de semana.  Esta curva contendrá 7 tuplas, por ejemplo
“fvdow”: [{“1”:0.9, “2”: 1.0, “3”: 0.9, “4”: 1.0, “5”:0.9, “6”:1.2, “7”:1.1 }]
c. Curva de variación anual (por mes del año): esta curva toma en cuenta la variación de la demanda de acuerdo a la época o regimen de cada mes del año, por lo que tendrá 12 valores.
“fvm”: [{“1”:1.0, “2”: 1.05, “3”: 1.1, “4”: 1.2, “5”: 1.15, “6”:1.05, “7”:1.1, “8”:, 0.95, “9”: 0.9, “10:, 0.85, “11”: 0.9, “12”: 0.95 }]
d.) Curva de variación de la producción
Este tipo de curva tendrá valores diferentes para las situaciones operativas que se puedan presentar en la producción, como por ejemplo: producción normal, producción de mantenimiento, fuera de operación, sobrecarga, producción de época seca, producción de época lluviosa.
 “fvp”: [{“normal”:1.0, “seca”: 0.9, “lluviosa”: 1.1, “mantenimiento”: 0.75, “f.o”: 0.0, “sobrecarga”:1.2 }]

Emisores
Los emisores son nudos especiales que permiten asignar un caudal de acuerdo a la presión en el nudo y a una ecuación de caudal en un orificio.  Cada emisor por lo tanto tendrá una ecuación diferente de acuerdo a la forma del orificio, su tamaño, el material y otras condiciones como si sale a la atmósfera o si sale al nivel freático, etc.
En sí, el nudo de tipo emisor, es un nudo que puede funcionar como nudo de demanda normal, pero es preferible que estos nudos no tengan un caudal asignado, con el fin de separar el efecto de emisor (fuga o caudal aportado por un hidrante) del efecto demanda, de modo que permita un mejor análisis.
Los tipos característicos de emisores son:
Hidrante
La ecuación de descarga de un hidrante está dada por:
                                      Q = Kv * (∆P)1/2
en donde Q es el caudal emitido, Kv es el coeficiente de descarga y ∆P es la caída de presión ó carga.  Si se supone que los hidrantes descargan a la atmósfera, dicha caída de carga equivale a la presión en el nodo.  Si descarga a un tanque o se succiona con una bomba, este valor de ∆P puede ser mayor o menor que la presión del nudo.   Para efectos prácticos se supondrá que ∆P=P.
Usualmente los caudales de hidrantes se trabajan en [m3/h] y las presiones en [bar], por lo que así se consignan los valores de Kv en la literatura, sin embargo, por congruencia con los cálculos del modelo, a continuación se proponen valores de Kv en hidrantes de acuerdo a la cantidad de bocas y sus diámetros en unidades de Q en [m³/s] y P en [m]:
Cantidad
D[mm]
D [in]
Kv
[m3/h] [bar]
Kv’
[m³/s] [mca]
1
50
2
33
2,871E-03
2
50
2
66
5,741E-03
1
75
3
80
6,959E-03
2
75
3
150
1,305E-02
1
100
4
180
1,566E-02

Fuga
Las fugas tienen una ecuación de funcionamiento que depende del tipo de fuga, su tamaño, el diámetro de la tubería, el material y la presión.  Esto hace que para cada fuga se deba consignar una ecuación diferente, cuya sorma es:


En el caso de los hidrantes γ toma un valor de 0.5, sin embargo en las fugas ese  parámetro puede variar desde 0 hasta 2
A continuación se muestra una propuesta de ambos valores para las fugas más recurrentes:
FALTA  (necesitamos una tesis)
Activar/Desactivar Bomba
Debe existir la capacidad de que durante la ejecución de un modelo en tiempo extendido, se pueda simular el encendido y apagado de una bomba.  Esto es posible mediante la asignación del estado del tramo intercambiándolo de bomba a check (BO -> CB, con CB en lugar de CK para diferenciarlo de un Check normal, que puede volver a funcionar como bomba en dado caso que vuelva a arrancar., o talvez más ordenado, incluir en la lista de opciones de la bomba un estado en la forma de un bit 0=apagado, 1=Encendido.  Este bit se concatenaría con los datos de la curva de la bomba:  
    • "opciones": "-3125.0 187.5 77.5 1" => α=-3125, β=187.5, γ=77.5 ON 
    • "opciones": "-3125.0 187.5 77.5 0" => α=-3125, β=187.5, γ=77.5 OFF 

Servidor tipo API
Ya incluidas las redes con todos los datos básicos
Pasarle los datos de niveles hora fecha y red a correr
