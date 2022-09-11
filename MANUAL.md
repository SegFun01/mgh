# Manual de MGH
## Método del Gradiente Hidráulico en Python
Programa para la modelación y simulación matemática de redes de distribución de agua a presión. Implementado en python3 usando  la metodología de análisis de redes propuesta por Pilati y Todini, 1987 
<hr>

## Work in progress !
#### Prof. Carlos Camacho Soto            
<br>

## Licencia y copyright
Publicado bajo la licencia GPL-3: GNU General Public License - versión 3 del 29 Junio de 2007 <br>
Copyright © 2022 Carlos Camacho Soto <br>
<br>
This file "MANUAL.md" is part of mgh <br>
mgh is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your option) any later version. <br>
mgh is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE.<br>
See the GNU General Public License for more details.<br>
You should have received a copy of the GNU General Public License along with mgh.<br> 
<br>

## Descripción

## Descarga e instalación
Se puede descargar directamente de GitHub, mediante:<br>
`git clone https://github.com/SegFun01/mgh.git`

Además, puede obtener un archivo comprimido desde: <br>
`https://github.com/SegFun01/mgh/archive/refs/heads/main.zip`

### Requerimientos
- python3
- python3-pip
- numpy

### Archivos incluidos
    .
    ├── f_hid.py
    ├── f_io.py
    ├── GradienteHidráulico.xlsx
    ├── img
    │   ├── Algoritmo_matrices_MGH.jpg
    │   ├── f01.png
    │   ├── f02.png
    │   ├── f03.png
    │   ├── f04.png
    │   ├── f05.png
    │   ├── f06.png
    │   ├── f07.png
    │   ├── f08.png
    │   ├── f09.png
    │   ├── f10.png
    │   ├── f11.png
    │   ├── f12.png
    │   ├── f13.png
    │   ├── f14.png
    │   ├── f15.png
    │   ├── f16.png
    │   └── f17.png
    ├── input
    │   ├── CaudalMax-kL.mgh
    │   ├── CaudalMax-kL.mgh.json
    │   ├── CaudalMax.mgh
    │   ├── CaudalMax.mgh.json
    │   ├── defaultC.mgh
    │   ├── default-error-topol.mgh
    │   ├── default-error-topol.mgh.json
    │   ├── default.mgh
    │   ├── default.mgh.json
    │   ├── EjemploBomba.mgh
    │   ├── EjemploBomba.mgh.json
    │   ├── EjemploVRP.mgh
    │   ├── EjemploVRP.mgh.json
    │   ├── EjemploVSP.mgh
    │   ├── EjemploVSP.mgh.json
    │   ├── Naciente.mgh
    │   ├── Naciente.mgh.json
    │   ├── P3Tanques.mgh
    │   ├── P3Tanques.mgh.json
    │   ├── pruebaJSON.mgh.json
    │   ├── Qmax-VR.mgh
    │   ├── Qmax-VR.mgh.json
    │   ├── Qmax-VS.mgh
    │   ├── Qmax-VS.mgh.json
    │   ├── Red-mixta.mgh
    │   └── Red-mixta.mgh.json
    ├── json_io.py
    ├── LICENSE
    ├── MANUAL.md
    ├── mghCSV.py
    ├── mghJSON.py
    ├── mgh.py
    ├── output
    │   ├── CaudalMax-kL.mgh.out
    │   ├── CaudalMax.mgh.out
    │   ├── defaultC.mgh.out
    │   ├── default.mgh.out
    │   ├── EjemploBomba.mgh.out
    │   ├── EjemploVRP-1.mgh.out
    │   ├── EjemploVRP.mgh.out
    │   ├── EjemploVRP.mgh.out.json
    │   ├── Naciente.mgh.out
    │   └── P3Tanques.mgh.out
    ├── __pycache__
    │   ├── f_global_var.cpython-39.pyc
    │   ├── f_hid.cpython-39.pyc
    │   ├── f_io.cpython-39.pyc
    │   └── json_io.cpython-39.pyc
    └── README.md

## Quick reference
#### Modo de uso
     
    python3 mgh.py nombre_archivo.mgh opcion 
                                                                              
    Opciones:                                               
    -n: modo normal, por defecto, imprime tablas de datos de entrada y salida.
    -q: modo silencioso, solo imprime los vectores H y Q finales.
    -v: modo detallado, imprime tablas de datos de entrada y salida, los vec-
        tores y matrices y los resultados de cada iteración. 
    -i: modo interactivo, permite construir y correr la red                                         
    
    Notas:
      La salida del programa va dirigida a la consola: "stdout"
      Si desea enviar a archivo use redirección con > o con >>
      La extensión y directorio de entrada por defecto son .mgh y ./input 
      
    Ejemplos:
      python3 mgh.py ./input/default.mgh -v > ./output/default.mgh.out
      python3 mgh.py default -n > ./output/default.mgh.out 
      python3 mgh.py ./input/default.mgh -q
      python3 mgh.py -i

## Creación de modelo
### Ingreso de datos

## Ejecución de una corrida de simulación
### Modos de ejecución

## Elementos
### Tipos de nudos
#### Nudos de carga fija
#### Nudos de demanda
#### Emisores
#### Fuentes constantes

### Tipos de tramos
#### Tubería simple
#### Accesorios especiales en tubería
#### Válvula de corte

## Ejecución en tiempo extendido

## Curvas de demanda
### Factor de variación horaria
### Factor de variación según día de la semana
### Factor de variación según mes
### Factor de variación según estación 

## Archivos de salida
### Salida por terminal en formato tabla
### Salida por archivo de texto en formato tabla
### Salida por archivo en formato .json
### Salida por stdout en formato .json

