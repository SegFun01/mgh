""" Archivo con la definición de las variables globales del método MGH
    Autor: Ing. Carlos Camacho Soto, ccamacho@segundafundacion.com
    Lugar: San José, Costa Rica
    Fecha: julio 2022
    f_global_var: variables globales con valores por defecto 
    
    Copyright © 2022 Carlos Camacho Soto

    This file "f_hid.py" is part of mgh
      mgh is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the 
      Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
      mgh is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
      or FITNESS FOR A PARTICULAR PURPOSE.
      See the GNU General Public License for more details.
      You should have received a copy of the GNU General Public License along with mgh. 
      If not, see <https://www.gnu.org/licenses/>. 
""" 

#---------->>>>>>>>>> Variables globales que se inicializan por defecto
fin = "input/default.mgh"       # archivo de entrada 
fout = fin + ".out"             # archivo de salida   
titulo= "Titulo de la red"      # titulo del modelo de red
autor= "Carlos Camacho Soto"    # autor del modelo
fecha= "21/03/1966"             # fecha de creacion
version= "1.0.0"                # version de la corrida a efectuar
viscosidad= 1.007E-6            # viscosidad cinematica en m2/s
imbalance= 1.0E-5               # desbalance de caudales permitido para convergencia
MaxIt= 40                       # cantidad de iteraciones de covergencia antes de abortar
ns= 1                           # cantidad de nudos de carga fija
n= 5                            # cantidad de nudos de demanda
t= 7                            # cantidad de tramos         
factor= 1                       # factor global de demanda del modelo  
modo="-n"                       # modo de impresión
ecuacion= "S"                   # Ecuación por defecto a usar Swamee-Jain, alternativa C=Colebrook-White
tol= 1E-6                       # tolerancia para el calculo de la f con Colebrok-White

#---------->>>>>>>>> Vectores de carga de datos desde el archivo
nn= []   # id de los nudos
e = []   # elevaciones de cada nudo
q = []   # demandas de los nudos (alturas de carga fija)
h = []   # cargas fijas en los nudos de carga fija
nt= []   # id de los tramos o tubos
de= []   # id del nudo de inicio del tramo
a = []   # id del nudo final del tramo
l = []   # longitudes de cada tramo en [m]
d = []   # diametro de cada tramo en [mm]
ks= []   # coeficiente de rugosidad del tra¿mo en [mm]
km= []   # coeficiente de perdidas locales del tramo
es= []   # estado del tramo: TA abierto, TC cerrado, BO bomba, VRP válvula, etc
tmp=[]   # temporal para guardar valores de las opciones del tramo
op= []   # opciones del tramo: presión de ajuste, alfa,beta,gama de la bomba
fi= []   # factores de variación horaria de cada nudo de demanda

