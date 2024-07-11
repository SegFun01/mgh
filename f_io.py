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
import time
import numpy as np
import json


# Hacer las funciones de impresión de salida aquí
# Hacer la función de revisión topológica aquí

#---------->>>>>>>>> Función que imprime el modo de uso
def uso():
   archivo_uso=open("uso.txt")
   print(archivo_uso.read())
   #print("")
   #print("                    METODO DEL GRADIENTE HIDRÁULICO              crcs 2022")
   #print("--------------------------------------------------------------------------")
   #print("")
   #print("Modo de uso:  python3 mgh.py nombre_archivo.mgh opcion")
   #print("")
   #print("Opciones:")
   #print("-n: modo normal, por defecto, imprime tablas de datos de entrada y salida")
   #print("-q: modo silencioso, solo imprime los vectores H y Q finales")
   #print("-v: modo detallado, imprime tablas de datos de entrada y salida, los vec-")
   #print("    tores y matrices y los resultados de cada iteración")
   #print("-i: modo interactivo, permite construir y correr la red")
   #print("")
   #print("Observaciones:")
   #print("  La salida del programa va dirigida a la consola: \"stdout\".")
   #print("  Si desea enviar a archivo use redirección con > o con >>")
   #print("  La extensión y directorio de entrada por defecto son .mgh y ./input")
   #print("")
   #print("Ejemplos:")
   #print("  python3 mgh.py ./input/default.mgh -v > ./output/default.mgh.out")
   #print("  python3 mgh.py default -n > ./output/default.mgh.out")
   #print("  python3 mgh.py ./input/default.mgh -q")
   #print("  python3 mgh.py -i")
   #print("-------------------------------------------------------------------------") */
#
#----------Fin de uso()

#---------->>>>>>>>>> Función para imprimir los datos de salida en modo quiet
def imprime_salida_quiet(Q,H,qfi,e,ns,fmt,dstn,fout):      # Imprime caudales en los tramos y presiones en los nudos de demanda
   orig_stdout = sys.stdout
   if fmt=="-t":
      fout = fout.replace(".json", ".txt")
      if dstn=="-f":
         f_sal= open(fout,"w")
         sys.stdout = f_sal 
      print("  [Q] l/s")
      for i in range(Q.size):
         print(f"| {(Q[i]*1000):7.2f} |")
      print("")   
      print("  [P] m")
      for i in range(H.size):
         print(f"| {(H[i]-e[i+ns]):7.2f} |")
      print("")
      print("  [Qo] l/s")
      for i in range(qfi.size):
         print(f"| {(qfi[i]*1000):7.2f} |")
      print("")
      if dstn=="-f":
         sys.stdout = orig_stdout 
         f_sal.close()
   if fmt=="-c":
      fout = fout.replace(".json",".csv")
      if dstn=="-f":
         f_sal= open(fout,"w")
         sys.stdout = f_sal 
      print("Caudales en tramos Q [l/s]")
      for i in range(Q.size):
         print(f"{i}, {Q[i]*1000:7.2f}")
      print("Presiones en nodos P [m]")
      for i in range(H.size):
         print(f"{i+ns}, {H[i]-e[i+ns]:7.2f}")
      print("Caudales en nudos de carga (Tanques/Embalses) Qo [l/s]")   
      for i in range(qfi.size):
         print(f"{i}, {qfi[i]*1000:7.2f}")
      print(f"timestamp,", time.strftime("%c"))   
      print(f"signature, crcs-2022")   
      if dstn=="-f":
         sys.stdout = orig_stdout 
         f_sal.close()   
   if fmt=="-j":
      q_dict = {}
      qt=[]
      ht=[]
      qit=[]
      for i in range(Q.size):
         qt.append({"id": i, "caudal": round(Q[i]*1000,2)})
      q_dict["caudal_tramos"]=qt
      for i in range(H.size):
         ht.append({"id": i+ns, "presion": round(H[i]-e[i-ns],2)})
      q_dict["presion_nudos"]=ht
      for i in range(qfi.size):
         qit.append({"id": i, "caudal": round(qfi[i]*1000,2)})      
      q_dict["caudal_tanques"]=qit
      q_dict["timestamp"]=time.strftime("%c")
      q_dict["signature"]="crcs-2022"
      # Serializing json
      json_object = json.dumps(q_dict, indent=4)
      if dstn=="-f":
         # Writing to sample.json
         with open(fout, "w") as outfile:
             outfile.write(json_object)
      else:
         print(json_object)
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
   np.set_printoptions(precision=2,linewidth=120)
   j=0
   for i in matrices:
      print(f"Matriz [{nombres[j]}]")
      print(f"{i}")
      print("")
      j=j+1

#---------->>>>>>>>>> Imprimir matrices de una lista
def imprime_matrices_2(matrices,nombres):
   # a partir de una lista de matrices y una lista de sus nombres imprime cada matriz de la lista
   np.set_printoptions(precision=2,linewidth=120)
   j=0
   for i in matrices:
      print(f"Matriz [{nombres[j]}]")
      print(f"{i.shape}")
      print("")
      j=j+1

#---------->>>>>>>>>> Imprimir lista de variables hidráulicas de los nudos
def imprime_hid(nt, de, a, l, d, ks, km, tp, op, At, v, Re, f, hf, hm, alfa,t):
   print("Variables hidráulicas de los tramos")   
   print("")
   print("  N  De->A    L    D    ks    kL    tp    A      v       Re     f       hf    hL      alfa")
   print("-------------------------------------------------------------------------------------------")
   for i in range(t):
       print(f"{nt[i]:>3} {de[i]:>3}{a[i]:>3} {l[i]:5.0f} {d[i]:4.0f} {ks[i]:5.4f} {km[i]:4.1f} {tp[i]:>3} {At[i]:7.4f} {v[i]:6.2f} {Re[i]:7.0f} {f[i]:6.5f} {hf[i]:6.2f} {hm[i]:5.2f} {alfa[i]:9.2f}" )
   print("-------------------------------------------------------------------------------------------")

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
   fout = fout.replace(".mgh","")
   fout = fout.replace(".json","")
   fout = "./output/" + fout  # se cambia el directorio por ./output/    
   fout = fout + ".mgh.out.json"       # se especifica extensión .mgh.out
   #print(fout)
   #x = input("Pausa en check output")
   return fout    

def crea_red():
   nn=[]
   e=[]
   q=[]
   nt=[]
   de= []   # id del nudo de inicio del tramo
   a = []   # id del nudo final del tramo
   l = []   # longitudes de cada tramo en [m]
   d = []   # diametro de cada tramo en [mm]
   ks= []   # coeficiente de rugosidad del tra¿mo en [mm]
   km= []   # coeficiente de perdidas locales del tramo
   es= []   # estado del tramo: TA abierto, TC cerrado, BO bomba, VRP válvula, etc
   tmp=[]   # temporal para guardar valores de las opciones del tramo
   tp=[]  # tipo de tramo
   op= []   # opciones del tramo: presión de ajuste, alfa,beta,gama de la bomba
   fi= []   # factores de variación horaria de cada nudo de demanda

   d_red = {}
   print("------> METODO DEL GRADIENTE HIDRÁULICO <-------")
   print("     Construcción de red en modo interactivo")
   print("-------------------------------------------------")
   fin = input("Escriba el nombre del archivo de entrada a crear: ")
   fin = input_check(fin)
   fin=fin+".json"
   print("-----")
   miVar = input("Título de la red a modelar: ")
   d_red["titulo"]=miVar
   miVar  = input("Autor del modelo          : ")
   d_red["autor"]=miVar
   miVar  = input("Fecha                     : ")
   d_red["fecha"]=miVar
   version = input("Versión de corrida        : ")
   d_red["version"]= miVar
   miVar = input("Viscosidad cinemática     : ")
   d_red["viscosidad"]=float(miVar)
   miVar = input("Desbalance de Q aceptado  : ")
   d_red["imbalance"]=float(miVar)
   miVar = input("Iteraciones permitidas    : ")
   d_red["max_iteraciones"]=int(miVar)
   miVar= input("Ecuación para f: C ó S    : ")
   d_red["ecuacion"]= miVar
   miVar= input("Tolerancia en cálculo de f: ")
   d_red["tolerancia"]= float(miVar)
   miVar = input("Factor global de demanda  : ")
   d_red["factor_demanda_global"]= float(miVar)
   print("----------------")
   ns = int(input("Cantidad de nodos de carga fija : "))
   print ("Nudo: Elevación,Carga,Hmax,Volumen")
   nc=[] 
   for i in range(ns):
      cadena = input(f"{i} : ")
      lista = cadena.split(",")
      nc.append({ "id": i, "elevacion": float(lista[0]), "carga":float(lista[1]), "altura":float(lista[2]), "volumen":float(lista[3])})
      # print(nc)
   d_red["nudos_carga"]= nc
   # print(d_red)
   nd = []
   # x = input("Pausa, pulse <enter>")
   print("----------------")
   n = int(input("Cantidad de nodos de demanda : "))
   print ("Nudo: Elevación,Demanda,Factor") 
   for i in range(n):
      cadena = input(f"{i+ns} : ")
      lista = cadena.split(",")
      nd.append({ "id": i+ns, "elevacion": float(lista[0]), "demanda": float(lista[1]), "factor": float(lista[2]) }) 
      # print(nd)
   d_red["nudos_demanda"]= nd 
   # print(d_red)
   # x = input("Pausa, pulse <enter>")
   t = int(input("Cantidad de tramos : "))
   print ("Tramo: de,a,L,D,Ks,KL,Tipo,Estado,Opciones") 
   tr =[]
   for i in range(t):
      cadena = input(f"{i}  :  ")
      lista = cadena.split(",")
      tr.append({ "id": i, "desde": int(lista[0]), "hasta": int(lista[1]), "longitud": float(lista[2]), "diametro": float(lista[3]), "ks":float(lista[4]), "kL": float(lista[5]), "tipo": lista[6], "opciones": lista[8], "estado":int(lista[7]) })  
   d_red["tramos"]= tr
   d_red["signature"]="#EOF- crcs-2022"
   #print(d_red)
   print("")
   # Serializing json
   json_red = json.dumps(d_red, indent=4)
   # x = input("Pausa, pulse <enter>")
   # print(json_red)
   # Writing to sample.json
   with open(fin, "w") as outfile:
      outfile.write(json_red)
   return fin

