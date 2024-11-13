# Programa para crear algoritmo de llenado y vaciado de tanque
#-
# Requiere las características del tanque, los caudales de salida y entrada (curva horaria)
# También se necesita la duración de la simulación en horas, el nivel inicial y la hora de inicio 
#
#---------->>>>>>>>>> Funcion para leer desde json

import math
import sys
import time
import numpy as np 
import json

qe = []   # caudales de entrada n valores (cantidad de valores de acuerdo al rango del análisis)
qs = []   # caudales de salida n valores (cantidad de valores de acuerdo al rango del análisis)
h = []    # niveles de tanque n valores (cantidad de valores de acuerdo al rango del análisis)
qa = []   # caudales aportados n valores (cantidad de valores de acuerdo al rango del análisis)
fin = "input/default.json"       # archivo de entrada 
fout = "output/default.out.json" # archivo de salida   
Ha = []  # niveles de tanque a cada hora (actuales)
ha = []  # horas actuales de los niveles actuales

# Se leen los datos desde un archivo .json
def leer_json(fin):
    global n,qe,qs,qa,hi,Hi,A,Hmax
    global titulo, autor, fecha, version, descripcion

    with open(fin,'r') as tq:
       j_tq = json.load(tq)
 
    titulo = j_tq.get('titulo')
    autor = j_tq.get('autor')
    fecha = j_tq.get('fecha')
    version = j_tq.get('version')
    descripcion = j_tq.get('descripcion')
    A = j_tq.get('area')
    Hmax = j_tq.get('altura')
    hi = j_tq.get('hora_inicio')
    Hi = j_tq.get('nivel_inicial')
    # n = j_tq.get('rango') no hace falta si se tienen todos l,os caudales, hora de inicio y nivel de inicio
   
    qe = j_tq['caudal_entrada']  
    qs = j_tq['caudal_salida']

    

def uso():
   print("")
   print("                    METODO DEL GRADIENTE HIDRÁULICO              crcs 2022")
   print("                      CÁLCULO DE NIVELES DE TANQUE                        ")
   print("--------------------------------------------------------------------------")
   print("")
   print("Modo de uso:  python3 nivel-tanque.py nombre_archivo.json")
   print("")
   print("La salida se dirige a STD, pero se hará salida json")
   print("")
   print("WIP")
   print("-------------------------------------------------------------------------") 
#----------Fin de uso()

#---------->>>>>>>>>> verificar nombre archivo entrada
def input_check(fin):
   if "/" not in fin:
      fin= "./input/" + fin # si no se especifica directorio se usa ./input por defecto
   if ".json" not in fin:
      fin = fin + ".json"    # si no se especifica extension se usa json por defecto
   return fin

#--------->>>>>>>>>>> verificar nombre archivo de salida
def output_check(fout):
   lista = fout.split("/")
   x = len(lista)
   fout = lista[x-1]
   fout = fout.replace(".json","")
   fout = "./output/" + fout + ".out.json" # se cambia el directorio por ./output/  y se agrega el distintivo out  
   #print(fout)
   #x = input("Pausa en check output")
   return fout   

# INICIO PROGRAMA

if len(sys.argv) < 2 :   #cuando solo se escribe mgh, imprime el modo de uso y termina
   uso()
   sys.exit()
else:                     #cuando se da el comando más un nombre de archivo, lo ejecuta en modo normal
   fin = sys.argv[1]
   fin = input_check(fin)
   fout = output_check(fin)

#-----Abrir el archivo: falta revisar si el archivo existe, si no, debe salir... 
try:
    f = open(fin,'r')
except:
    print("--------------------------------------------------")
    print("        MÉTODO DEL GRADIENTE HIDRÁULICO")
    print("--------------------------------------------------")
    print("Archivo de entrada:", fin)
    print("¡Ocurrió un error al abrir el archivo !!!")
    print("Programa abortado")
    print("--------------------------------------------------")
    sys.exit()    
#-----Cargar los datos globales de la corrida
f.close()
leer_json(fin)

ha.append(hi)
Ha.append(Hi)

for i in range(len(qs)):
   qa.append(qe[i]-qs[i]) 
   dH = qa[i]*3.6/A
   hh=ha[i]+1
   if hh>23 :
      hh=0
   ha.append(hh)
   Ha.append(Ha[i]+dH)


print("caudales de entrada")
print(qe)

print("caudales de salida")
print(qs)

print("horas, caudales aportados y niveles")
print(ha)
print(qa)
print(Ha)

