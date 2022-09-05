""" Archivo con las funciones de entrada y salida y otras varias de MGH
    Autor: Ing. Carlos Camacho Soto, ccamacho@segundafundacion.com
    Lugar: San José, Costa Rica
    Fecha: julio 2022
    f_io.py: funciones de impresión y otras varias
    
    Copyright © 2022 Carlos Camacho Soto

    This file "f_io.py" is part of mgh
      mgh is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the 
      Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
      mgh is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
      or FITNESS FOR A PARTICULAR PURPOSE.
      See the GNU General Public License for more details.
      You should have received a copy of the GNU General Public License along with mgh. 
      If not, see <https://www.gnu.org/licenses/>. 
"""

#import math
import sys
import numpy as np


# Hacer las funciones de impresión de salida aquí
# Hacer la función de revisión topológica aquí

#---------->>>>>>>>> Función que imprime el modo de uso
def uso():
   print("")
   print("                    METODO DEL GRADIENTE HIDRÁULICO              crcs 2022")
   print("--------------------------------------------------------------------------")
   print("")
   print("Modo de uso:  python3 mgh.py nombre_archivo.mgh opcion")
   print("")
   print("Opciones:")
   print("-n: modo normal, por defecto, imprime tablas de datos de entrada y salida")
   print("-q: modo silencioso, solo imprime los vectores H y Q finales")
   print("-v: modo detallado, imprime tablas de datos de entrada y salida, los vec-")
   print("    tores y matrices y los resultados de cada iteración")
   print("")
   print("Observaciones:")
   print("  La salida del programa va dirigida a la consola: \"stdout\".")
   print("  Si desea enviar a archivo use redirección con > o con >>")
   print("  La extensión y directorio de entrada por defecto son .mgh y ./input")
   print("")
   print("Ejemplos:")
   print("  python3 mgh.py ./input/default.mgh -v > ./output/default.mgh.out")
   print("  python3 mgh.py default -n > ./output/default.mgh.out")
   print("  python3 mgh.py ./input/default.mgh -q")
   print("-------------------------------------------------------------------------")
#----------Fin de uso()

#---------->>>>>>>>>> Función para imprimir los datos de salida en modo quiet
def imprime_salida_quiet(Q,H,e,ns):      # Imprime caudales en los tramos y presiones en los nudos de demanda
   print("  [Q] l/s")
   for i in range(Q.size):
      print(f"| {(Q[i]*1000):7.2f} |")
   print("")   
   print("  [P] m")
   for i in range(H.size):
      print(f"| {(H[i]-e[i+ns]):7.2f} |")
   print("") 
  
#-----------

#---------->>>>>>>>>> Función que imprime la salida normal: tablas de nudos y tramos
def imprime_salida_normal():
      print("normal: Imprime reporte final")   
#----------      

#---------->>>>>>>>>> Función que imprime las matrices de cada iteración
def imprime_salida_verbose(final,i):
   if final:
      io.imprime_salida_normal()
   else:
      print("Imprime matrices y vectotres de iteración i")
#----------

#---------->>>>>>>>>> Función que revisa la topología de la red, termina si hay error y lo indica
def revisar_topologia(t,fin,n,ns,nn,de,a,titulo,autor,fecha,version,modo):
   notOK=[]
   errores=0
   for i in range(n+ns):
      nudosOK=False
      for j in range(t):
         if de[j]==nn[i] or a[j]==nn[i]:
            nudosOK=True
      if nudosOK==False:
         notOK.append(nn[i])
         errores= errores+1       
   if errores>0:
      print("--")
      print("MÉTODO DEL GRADIENTE HIDRÁULICO")
      print("--")
      print("Archivo de entrada:", fin)
      print("Titulo:     ",titulo)
      print("Autor:      ",autor)
      print("Fecha:      ",fecha)
      print("Versión:    ",version)
      print("--")
      print("Error en la topología de nudos y tramos: nudos sin conexión")
      print("Revise los siguientes nudos: ",notOK)
      print("--")
      sys.exit()
   if modo =="-v":   
     print("Topología de nudos OK")
     print("")
#----------

#---------->>>>>>>>>> Imprimir matrices de una lista
def imprime_matrices(matrices,nombres):
   # a partir de una lista de matrices y una lista de sus nombres imprime cada matriz de la lista
   j=0
   for i in matrices:
      print(f"Matriz [{nombres[j]}]")
      print(f"{i}")
      print("")
      j=j+1

#---------->>>>>>>>>> Imprimir matrices de una lista
def imprime_matrices_2(matrices,nombres):
   # a partir de una lista de matrices y una lista de sus nombres imprime cada matriz de la lista
   j=0
   for i in matrices:
      print(f"Matriz [{nombres[j]}]")
      print(f"{i.shape}")
      print("")
      j=j+1

#---------->>>>>>>>>> Imprimir lista de variables hidráulicas de los nudos
def imprime_hid(nt, de, a, l, d, ks, km, es, op, At, v, Re, f, hf, hm, alfa,t):
   print("Variables hidráulicas de los tramos")   
   print("")
   print("  N  De->A    L    D    ks    kL    Es    A     v      Re     f       hf    hL     alfa")
   print("----------------------------------------------------------------------------------------")
   for i in range(t):
       print(f"{nt[i]:>3} {de[i]:>3}{a[i]:>3} {l[i]:5.0f} {d[i]:4.0f} {ks[i]:5.4f} {km[i]:4.1f} {es[i]:>3} {At[i]:7.4f} {v[i]:4.2f} {Re[i]:7.0f} {f[i]:6.5f} {hf[i]:5.2f} {hm[i]:5.2f} {alfa[i]:8.2f}" )
   print("----------------------------------------------------------------------------------------")

#---------->>>>>>>>>> Imprimir matrices para verificación
def matrices_check(Ho,qi,H,Q,B,BT,C,I,N,At,v,Re,f,hf,hm,alfa,A,A1):
  print("Matriz cargas fijas:",Ho) 
  print("Matriz demandas:",qi) 
  print("Matriz de cargas en nudos:",H)
  print("Matriz de caudales en los tramos: Q")
  print(Q)
  print("Topología nudos de carga fija: C")
  print(C)
  print("Topología de tramos-nudos: B")
  print(B)
  print("Transpuesta de B: BT")
  print(BT)
  print("Matriz identidad: I")
  print(I)
  print("Matriz de potencias de la ecuación de pérdidas: N")
  print(N)
  print("Areas de los tramos: At") 
  print(At)
  print("Velocidades en los tramos: v")
  print(v)
  print("Número de Reynolds de los tramos: Re")
  print(Re)
  print("Coeficientes de pérdidas de los tramos: f")
  print(f)
  print("Pérdidas por fricción en los tramos: hf")
  print(hf)
  print("Pérdidas locales en los tramos: hm")
  print(hm)
  print("Coeficientes alfa de los tramos: alfa")
  print(alfa)
  print("Matriz de valores alfa: A")
  print(A)
  print("Matriz de valores alfa: A'")
  print(A1)
#----------

#---------->>>>>>>>>> verificar nombre archivo entrada
def input_check(fin):
   if "/" not in fin:
      fin= "./input/" + fin # si no se especifica directorio se usa ./input por defecto
   if ".mgh" not in fin:
      fin = fin + ".mgh"    # si no se especifica extension se usa mgh por defecto
   return fin

#--------->>>>>>>>>>> verificar nombre archivo de salida
def output_check(fout):
   lista = fout.split("/")
   x = len(lista)
   fout = lista[x-1]
   fout = "./output/" + fout  # se cambia el directorio por ./output/    
   fout = fout + ".out"       # se especifica extensión .mgh.out
   return fout    

def crea_red(fout):
   nn=[]
   e=[]
   q=[]
   f=[]
   nt=[]
   print("------> METODO DEL GRADIENTE HIDRÁULICO <-------")
   print("     Construcción de red en modo interactivo")
   titulo = input("Título de la red a modelar: ")
   autor  = input("Autor del modelo          : ")
   fecha  = input("Fecha                     : ")
   version = input("Versión de corrida       : ")
   viscosidad = float(input("Viscosidad cinemática :"))
   imbalance = floar(input("Desbalance de caudales aceptado : "))
   MaxIt = int(input("Cantidad de iteraciones permitidas : "))
   ecuacion= input("Ecuación para f [C/S]: ")
   print("----------------")
   ns = int(input("Cantidad de nodos de carga fija : "))
   print ("Nudo  Elev.   Carga ") 
   for i in range(ns):
      cadena = input("{i} :")
      lista = cadena.strip()
      nn.append(i)
      e.append(float(lista[0]))
      q.append(float(lista[1]))
   print("----------------")
   n = int(input("Cantidad de nodos de demanda : "))
   print ("Nudo  Elev. Demanda Factor ") 
   for i in range(n):
      cadena = input("{i+ns} :")
      lista = cadena.strip()
      nn.append(i+ns)
      e.append(float(lista[0]))
      q.append(float(lista[1]))
      f.append(float(lista[2]))
   t = int(input("Cantidad de tramos : "))
   print ("Nudo  Elev. Demanda Factor ") 
   for i in range(t):
      cadena = input("{i+ns} :")
      lista = cadena.strip()
      nn.append(i+ns)
      e.append(float(lista[0]))
      q.append(float(lista[1]))
      f.append(float(lista[2]))