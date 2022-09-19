""" Modelado de redes hidráulicas por el método del gradiente hidráulico
    Autor: Ing. Carlos Camacho Soto, ccamacho@segundafundacion.com
    Lugar: San José, Costa Rica
    Fecha: julio 2022

    Copyright © 2022 Carlos Camacho Soto
    Publicado bajo licencia GPL v3.0

    This file "mgh.py" is part of mgh
      mgh is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the 
      Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
      mgh is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
      or FITNESS FOR A PARTICULAR PURPOSE.
      See the GNU General Public License for more details.
      You should have received a copy of the GNU General Public License along with mgh. 
      If not, see <https://www.gnu.org/licenses/>. 
"""
#! /usr/bin/env python

#---------->>>>>>>>>> Importar archivos y librerías
import math
import sys
import time
import numpy as np 
import f_hid as hid   # funciones hidráulicas
import f_io as io     # funciones de impresion
import json
#import json_io as jio # funciones de entrada y salida de datos en JSON


#---------->>>>>>>>>> Variables globales que se inicializan por defecto
fin = "input/default.mgh"       # archivo de entrada 
fout = "output/default.mgh.out" # archivo de salida   
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
fmt="-t"                        # formato de salida
dstn="-s"                       # destino de salida
inter=False                     # modo interactivo
ecuacion= "S"                   # Ecuación por defecto a usar Swamee-Jain, alternativa C=Colebrook-White
tol= 1E-6                       # tolerancia para el calculo de la f con Colebrok-White
orig_stdout=sys.stdout          # guarda la salida por defecto de stdout

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
es= []   # estado del tramo: 1=ON, 0=OFF
tmp=[]   # temporal para guardar valores de las opciones del tramo
op= []   # opciones del tramo: presión de ajuste, alfa,beta,gama de la bomba
fi= []   # factores de variación horaria de cada nudo de demanda
tp=[]    # tipo de tramo TB, EM, VS, VR, CK, BO, VQ

#---------->>>>>>>>>> Funcion para leer desde json
def leer_json(fin):
    global nn,nt,e,q,fi,h,de,a,l,d,ks,km,es,op
    global titulo, autor, fecha, version, viscosidad, descripcion
    global imbalance, MaxIt, factor, ecuacion, tol, duracion
    global ns, n, t 
    with open(fin,'r') as red:
       j_red = json.load(red)
    # print(j_red)
    # x=input("pulse enter")
    ns = len(j_red['nudos_carga'])
    n  = len(j_red['nudos_demanda'])
    t  = len(j_red['tramos'])
    # print(ns , n , t)
    # x=input("pulse enter")
    titulo = j_red.get('titulo')
    autor = j_red.get('autor')
    fecha = j_red.get('fecha')
    version = j_red.get('version')
    viscosidad = j_red.get('viscosidad')
    imbalance = j_red.get('imbalance')
    MaxIt = j_red.get('max_iteraciones')
    tol = j_red.get('tolerancia')
    factor = j_red.get('factor_demanda_global')
    ecuacion = j_red.get('ecuacion')
    duracion = j_red.get('duracion')
    descripcion = j_red.get('descripcion')
    
    for i in (j_red['nudos_carga']): # leer los nudos de carga del JSON
       nn.append(i.get('id'))
       e.append(i.get('elevacion'))
       q.append(i.get('carga'))
       h.append(i.get('carga'))  

    for i in (j_red['nudos_demanda']): # leer los nudos de demanda del JSON
       nn.append(i.get('id'))
       e.append(i.get('elevacion'))
       q.append(i.get('demanda'))
       fi.append(i.get('factor'))

    for i in (j_red['tramos']):  # leer los tramos del JSON
       nt.append(i.get('id'))
       de.append(i.get('desde'))
       a.append(i.get('hasta'))
       l.append(i.get('longitud'))
       d.append(i.get('diametro'))
       ks.append(i.get('ks'))
       km.append(i.get('kL'))
       es.append(i.get('estado'))
       op.append(i.get('opciones'))
       tp.append(i.get('tipo'))

#---------->>>>>>>>>> Carga de datos desde archivo JSON,    CSV deprecado
def asigna_modo(opcn):     # función para definir el modo de ejecución del programa 
   if "q" in opcn:
      modo="-q"
   elif "v" in opcn:
      modo="-v"
   else:
      modo="-n"
   return modo

def asigna_fmt(opcn):      # función para definir el formato de salida: JSON, CSV ó TXT
   if "j" in opcn:
      fmt="-j"
   elif "c" in opcn:
      fmt="-c"
   else:
      fmt="-t"
   return fmt

def asigna_dstn(opcn):     # escoger el medio de salida: terminal o archivo
   if "f" in opcn:
      dstn="-f"
   else:
      dstn="-s"
   return dstn

def asigna_inter(opcn):    # define si se ingresa en modo interactivo
   if "i" in opcn:
      inter=True
   else:
      inter=False
   return inter

#-----Verificar los parámetros de entrada
if len(sys.argv) < 2 :   #cuando solo se escribe mgh, imprime el modo de uso y termina
   io.uso()
   fin = ".input/default.mgh.json"
   sys.exit()
else:                     #cuando se da el comando más un nombre de archivo, lo ejecuta en modo normal
   fin = sys.argv[1]
   fin = io.input_check(fin)
   if ".json" not in fin:
      fin = fin + ".json"
   fout = io.output_check(fin)
   #print(f"F input: {fin}   F output: {fout} ")
   modo = "-n"
if len(sys.argv) == 3 :  #se da comando, archivo, modo
   opcn = sys.argv[2]
   opcn.strip()
   modo=asigna_modo(opcn)
   # print(f"Modo {modo}")
   fmt= asigna_fmt(opcn)
   # print(f"Formato {fmt}")
   dstn=asigna_dstn(opcn)
   # print(f"Destino {dstn}")
   inter=asigna_inter(opcn)
   # print(f"Interactivo {inter}")
   # parada=input("Pulse enter.... o ctrl-c")
#antes de abrir archivo verificar si se desea incluir datos interactivamente
if inter:
    fin = io.crea_red()
    fout = io.output_check(fin)

#---> Si la salida se envía a archivo se debe redirigir stdout
if dstn=="-f" and fmt=="-t" and modo=="-v":
   fout_txt= fout.replace(".json",".txt")
   f_sal= open(fout_txt,"w")
   sys.stdout = f_sal 

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

#---------->>>>>>>>>> Revisar topología de la red
if modo=="-v":
   print("MÉTODO DEL GRADIENTE HIDRÁULICO")
   print("")
   print("Modo de ejecución: Impresión detallada")
   print("--")   
   
io.revisar_topologia(t,fin,n,ns,nn,de,a,titulo,autor,fecha,version,modo)
        
#---------->>>>>>>>>> Definicion de matrices globales del MGH
qi = np.zeros(n,dtype=float)       # caudales demandados en los nodos
Ho = np.zeros(ns,dtype=float)      # cargas fijas
H = np.zeros(n,dtype=float)        # cargas dinamicas en los nudos
C = np.zeros([t,ns],dtype=float)   # topologia tramos x nudos de carga fija [t x ns]
B = np.zeros([t,n],dtype=float)    # topologia nudo a tramo  [t x n]
BT= np.zeros([n,t],dtype=float)    # transpuesta de B [n x t] esta matriz no se requiere
#A1= np.zeros([t,t],dtype=float)    # matriz de valores Alfa de modo que hf=alfa*Q  ->A11'
#A = np.zeros([t,t],dtype=float)    # matriz de valores Alfa para accesorios especiales (bomba y válvula)
I = np.identity(t,dtype=float)     # matriz identidad [t x t]
N = np.zeros([t,t],dtype=float)    # exponentes de la ecuación de pérdidas, 2 en Darcy Weisbach
Q = np.zeros([t],dtype=float)      # caudales en los tramos [m3/s]
At= np.zeros([t],dtype=float)      # áreas de las tuberías en [m2]
v = np.zeros([t],dtype=float)      # velocidades del flujo en los tubos [m/s]
Re= np.zeros([t],dtype=float)      # números de Reynolds ern los tramos
f = np.zeros([t],dtype=float)      # factores de fricción de D-W de cada tramo
hf= np.zeros([t],dtype=float)      # pérdidas por fricción de cada tramo en [m]
hm= np.zeros([t],dtype=float)      # pérdidas locales de cada tramo en [m]
alfa=np.zeros([t],dtype=float)     # valores alfa de cada tramo
beta=np.zeros([t],dtype=float)     # valores beta de cada tramo para usar en A11
gama=np.zeros([t],dtype=float)     # valores gama de cada tramo para usar en A11
Hi = np.zeros(n,dtype=float)       # cargas dinamicas en los nudos de la actual iteración
Qi = np.zeros([t],dtype=float)     # caudales en los tramos [m3/s] en la actual iteración
qfi = np.zeros(ns,dtype=float)     # caudales en los nudos de carga fija

### AQUI SE DEBE INICIAR UN CICLO QUE ITERE EL CÁLCULO COMPLETO SI CAMBIA LA TOPOLOGÍA
### DE LA RED O SI SE REALIZA UN ANÁLISIS EN TIEMPO EXTENDIDO
### while ok:    ok se alcanza si la red no requiere cerrar check, o si se acabaron las iteraciones

#---------->>>>>>>>>> Iniciar matrices: carga de los datos en las matrices a partir de los vectores de lectura
Q.fill(0.1)                          # iniciar caudales en tramos
np.fill_diagonal(N,2)                # iniciar matriz N con 2 en la diagonal
for i in range(0,ns):                
    Ho[i]=(h[i])                     # iniciar matriz alturas fijas 
for i in range(ns,n+ns):
    qi[i-ns]=(q[i]/1000*factor*fi[i-ns]) # iniciar matriz demandas en nudos   
for i in range(t):
    #if tp[i]=="EM":
    #   N[i,i]=float(op[i])  op tiene 2 valores Kv y gama, hay que hacer un split 
    for j in range(ns):
        if de[i]==j and es[i]==1:
            C[i,j]=-1                  # iniciar matriz topológica de cargas fijas nudo de salida=-1
        if a[i]==j and es[i]==1:
            C[i,j]=1                   # iniciar matriz topológica de cargas fijas nudo de llegada =-1
    for j in range(ns,ns+n):           # construye la matriz de topología de nudo a tramo
      if es[i]==1:                     # solo asigna los nudos de entrada y salida si el tubo está abierto
        jj=j-ns
        if de[i]==j:
            B[i,jj]= -1.0             # asigna el nudo de entrada a la tubería
        if a[i]==j:
            B[i,jj]= 1.0              # asigna el nudo de sdalida a la tubería 
    At[i]=hid.area(d[i])             # iniciar matriz Areas de Tubos
    v[i]=hid.ve(Q[i],At[i])          # iniciar matriz de velocidades en tubos
    Re[i]=hid.reynolds(v[i],d[i],viscosidad) # iniciar matriz Reynolds
    f[i]= hid.fCW(ks[i],d[i],Re[i],tol,ecuacion)    # iniciar matriz factor fricción usando Colebrook-White/Swamee-Jain
    hf[i]=hid.hfr(f[i],l[i],v[i],d[i])       # iniciar matriz pérdidas fricción
    hm[i]=hid.hme(km[i],v[i])                # iniciar matriz pérdidas locales 
    alfa[i]=hid.alf(hf[i]+hm[i],Q[i])        # Iniciar matriz de alfas
BT = np.transpose(B)                         # iniciar matriz B transpuesta
A1= hid.construir_A1(alfa,Q,t,tp,op)               #iniciar matriz A'
A = hid.construir_A(A1,t,tp,op,e,de,a,hf,hm,H,Q,modo,ns) # iniciar matriz A       
#---------->>>>>>>>>> Check de matrices:   comentar
#io.matrices_check(Ho,qi,H,Q,B,BT,C,I,N,At,v,Re,f,hf,hm,alfa,A,A1)


#---> DEFINICION DE FUNCIONES GOLABLES --------------------------------

#---> RECALCULAR las matrices v, Re, f, hf, hm para obtener el alfa en cada iteración
def recalcular_alfa():
   global v,Re,f,hf,hm,alfa
   for i in range(t):
       v[i]= hid.ve(Q[i],At[i])
       Re[i]=hid.reynolds(v[i],d[i],viscosidad)
       f[i]= hid.fCW(ks[i],d[i],Re[i],tol,ecuacion)        # f usando Colebrook-White/Swamee-Jain
       hf[i]=hid.hfr(f[i], l[i], v[i], d[i]) 
       hm[i]= hid.hme(km[i],v[i])
       alfa[i]=hid.alf(hf[i]+hm[i],Q[i])

#---> Algoritmo de solución de las matrices [Hi] y [Qi]
def calcula_Hi_Qi():
   global Qi, Hi  # matrices que se modifican
   # - paso 1 
   M3= np.matmul(N,A1)
   M4= np.matmul(A,Q)
   M5= np.matmul(C,Ho)
   # - paso 2
   M3= np.linalg.inv(M3)
   M4= np.add(M4,M5)
   # - paso 3
   M1= np.matmul(BT,M3)
   # - paso 4
   M2= np.matmul(M1,M4)
   # - paso 5
   M1= np.matmul(M1,B)
   M4= np.matmul(BT,Q)
   # - paso 6
   M1= np.linalg.inv(M1)
   M4= np.subtract(M4,qi)
   # - paso 7
   M1= M1*(-1)
   M2= np.subtract(M2,M4)
   # - paso 8
   Hi = np.matmul(M1,M2)  # primer resultado
   # - paso 9
   M1= np.matmul(M3,A)
   M4= np.matmul(B,Hi)
   # - paso 10   
   M1= np.subtract(I,M1)
   M4= np.add(M4,M5)
   # - paso 11
   M1= np.matmul(M1,Q)
   M2= np.matmul(M3,M4)
   # - paso 12
   Qi= np.subtract(M1,M2) # segundo resultado

#---> verificar si hay un check y si q<0 cerrarlo
def revisaChecks():
  cambio=False
  for i in range(t):
     if tp[i]=="CK" or tp[i]=="BO":
       if Qi[i]<0:
          es[i]=0
          cambio=True
          dqT=1
  return cambio

#---> reconstruir matriz B si se cierra un tubo
def cierra_check():
  global C, B, BT
  for i in range(t):
     for j in range(ns):
       if de[i]==j and es[i]==0:
            C[i,j]=0                  # reescribir en matriz topológica de cargas fijas nudo de salida=-1
       if a[i]==j and es[i]==0:
           C[i,j]=0
     for j in range(ns,ns+n):           # construye la matriz de topología de nudo a tramo
         jj=j-ns
         if de[i]==j and es[i]==0:
             B[i,jj]= 0
         if a[i]==j and es[i]==0:
             B[i,jj]= 0
  BT = np.transpose(B)
  

#---> Impresión de reporte final
def imprime_reporte():                       # pasar a f_io con valores de entrada 
   print("MÉTODO DEL GRADIENTE HIDRÁULICO              v1.0.0-alpha")
   print("")
   print("Archivo de entrada:", fin)
   print("Titulo:     ",titulo)
   print("Autor:      ",autor)
   print("Fecha:      ",fecha)
   print("Versión:    ",version)
   print("Viscosidad: ",viscosidad)
   print("Desbalance: ",imbalance)
   print("Máximo iteraciones permitidas: ",MaxIt)
   if ecuacion=="C":
      print("Ecuación de pérdidas de fricción: Colebrook-White")
   else:
      print("Ecuación de pérdidas de fricción: Swamee-Jain")
   print("Factor global de demanda: ", factor)
   print("")
   print("DATOS DE ENTRADA")
   print("")
   print("Nudos de carga fija")
   print("  N  Elevación    Carga    Nivel")
   print("---------------------------------")
   for i in range(ns):
      print(f"{nn[i]:>3}  {e[i]:7.2f}    {h[i]:7.2f}  {(h[i]-e[i]):7.2f} ")
   print("---------------------------------")
   print("")
   print("Nudos de demanda")
   print("  N  Elevación   Demanda    FVH")
   print("---------------------------------")
   for i in range(n):
      print(f"{nn[i+ns]:>3}  {e[i+ns]:7.2f}    {q[i+ns]:7.2f}   {fi[i]:6.2f} ")
   print("---------------------------------")
   print("")
   print("Tramos")
   print("  T   de->a      L     D     A       ks     kL   Tipo    Op ")
   print("---------------------------------------------------------------")
   for i in range(t):
      print(f"{nt[i]:>3}  {de[i]:>3}{a[i]:>3} {l[i]:7.0f} {d[i]:5.0f} {At[i]:7.4f}  {ks[i]:5.4f} {km[i]:5.1f}   {tp[i]:>3}   {op[i]} ")
   print("---------------------------------------------------------------")
   print("")   
   print("RESULTADOS")
   print("")
   print("Nudos de carga fija")  
   print("  N  Elevación    Carga    Nivel   Caudal")
   print("------------------------------------------")
   for i in range(ns):
       print(f"{nn[i]:>3}  {e[i]:7.2f}    {h[i]:7.2f}  {(h[i]-e[i]):7.2f}  {(qfi[i]*1000):7.2f}")
   print("------------------------------------------")
   print("")
   print("Nudos de demanda")
   print("  N  Elevación   Q Base    FVH    Q Neto      Carga   Presión")
   print("-------------------------------------------------------------")
   for i in range(n):
       print(f"{nn[i+ns]:>3}  {e[i+ns]:7.2f}    {q[i+ns]:7.2f}  {fi[i]:6.2f}  {(qi[i]*1000):7.2f}    {H[i]:7.2f}  {(Hi[i]-e[i+ns]):7.2f}")
   print("-------------------------------------------------------------")
   print("")
   print("Tramos")
   print("  T   de->a      V       Q       hf      hL      hT       S   ")
   print("---------------------------------------------------------------")    
   for i in range(t):
       if "VR" in tp[i] or "VS" in tp[i] or "BO" in tp[i]:  # si hay un accesorio imprime la carga del accesorio
          hv =  f'{((A1[i,i]-A[i,i])*Qi[i]):.2f}'
          hv = "H"+ tp[i].strip() + "=" + hv
       else:
          hv=""
       print(f"{nt[i]:>3}  {de[i]:>3}{a[i]:>3}   {v[i]:6.2f}  {(Qi[i]*1000):6.2f}  {hf[i]:6.2f}  {hm[i]:6.2f}  {(hf[i]+hm[i]):6.2f}   {((hf[i]+hm[i])/l[i]):7.5f} {hv}")
       
   print("---------------------------------------------------------------")    
   print("")
   print("Fecha y hora de esta corrida: ",time.strftime("%c"))
   print("crcs-2022")
#----------------------------------------------------------------------

#--------------------->>>>>>>>>>>> Imprimir salida en formato json a archivo
def imprime_salida_json(fout):
   d_red={}
   d_red["titulo"]=titulo
   d_red["autor"]=autor
   d_red["fecha"]=fecha
   d_red["version"]= version
   d_red["viscosidad"]=float(viscosidad)
   d_red["imbalance"]=float(imbalance)
   d_red["max_iteraciones"]=int(MaxIt)
   d_red["ecuacion"]= ecuacion
   d_red["tolerancia"]= tol
   d_red["factor_demanda_global"]= float(factor)
   #-----Lee los nudos de carga fija
   nc = []
   for i in range(0,ns):
      nc.append({ "id": nn[i], "elevacion": e[i], "carga": q[i], "nivel": e[i]-q[i], "caudal": round(qfi[i]*1000,2) })
   d_red["nudos_carga"]=nc
   #-----Leer los nudos de demanda
   nd=[]
   for i in range(0,n):
      nd.append({ "id": nn[i+ns], "elevacion": e[i+ns], "demanda": q[i+ns],"factor": fi[i], "demanda_neta": qi[i]*1000, "altura_piezometrica": round(Hi[i],2), "presion": round(Hi[i]-e[i+ns],2) })
   d_red["nudos_demanda"]=nd
   #-----Leer los datos de los tramos
   tr=[]
   for i in range(0,t):
      if "VR" in tp[i] or "VS" in tp[i] or "BO" in tp[i]:  # si hay un accesorio imprime la carga del accesorio
          hv =  ((A1[i,i]-A[i,i])*Qi[i])
      else:
          hv=0
      tr.append({ "id": nt[i], "desde": de[i], "hasta": a[i], "longitud": l[i], "diametro": d[i],"ks": ks[i],"kL": km[i],"tipo": tp[i],"opciones": op[i],"estado":es[i], "caudal": round(Qi[i]*1000,2), "velocidad": round(v[i],2), "Re": round(Re[i],2), "f": f[i], "hf": round(hf[i],2), "hL": round(hm[i],2), "h_accesorio": round(hv,2) })
   d_red["tramos"]=tr
   d_red["signature"]="crcs-2022"
   d_red["timestamp"]=time.strftime("%c")
   
   # Serializing json
   json_object = json.dumps(d_red, indent=4)
   if dstn=="-f":
      # Writing to sample.json
      with open(fout, "w") as outfile:
          outfile.write(json_object)
   else:
      print(json_object)

#---> Impresión de reporte final en CSV
def imprime_reporte_csv():                       # pasar a f_io con valores de entrada 
   print("MÉTODO DEL GRADIENTE HIDRÁULICO v1.0.0-alpha")
   print("Titulo,",titulo)
   print("Autor,",autor)
   print("Fecha,",fecha)
   print("Versión,",version)
   print("Viscosidad,",viscosidad)
   print("Desbalance,",imbalance)
   print("Máximo iteraciones,",MaxIt)
   if ecuacion=="C":
      print("Ecuación, Colebrook-White")
   else:
      print("Ecuación,Swamee-Jain")
   print("Factor global,", factor)
   print("DATOS DE ENTRADA")
   print("Nudos de carga fija")
   print("N, Elevación, Carga, Nivel")
   for i in range(ns):
      print(f"{nn[i]:>3}, {e[i]:7.2f}, {h[i]:7.2f}, {(h[i]-e[i]):7.2f}")
   print("Nudos de demanda")
   print("N, Elevación, Demanda, FVH")
   for i in range(n):
      print(f"{nn[i+ns]:>3}, {e[i+ns]:7.2f},{q[i+ns]:7.2f},{fi[i]:6.2f}")
   print("Tramos")
   print("T, desde, hasta, L, D, A, ks, kL, tipo, Op")
   for i in range(t):
      print(f"{nt[i]:>3}, {de[i]:>3}, {a[i]:>3}, {l[i]:7.0f}, {d[i]:5.0f}, {At[i]:7.4f}, {ks[i]:5.4f}, {km[i]:5.1f}, {tp[i]:>3}, {op[i]}")
   print("RESULTADOS")
   print("Nudos de carga fija")  
   print("N, Elevación, Carga, Nivel, Caudal")
   for i in range(ns):
       print(f"{nn[i]:>3}, {e[i]:7.2f}, {h[i]:7.2f}, {(h[i]-e[i]):7.2f}, {(qfi[i]*1000):7.2f}")
   print("Nudos de demanda")
   print("N, Elevación, Q Base, FVH, Q Neto, Carga, Presión")
   for i in range(n):
       print(f"{nn[i+ns]:>3}, {e[i+ns]:7.2f}, {q[i+ns]:7.2f}, {fi[i]:6.2f}, {(qi[i]*1000):7.2f}, {H[i]:7.2f}, {(Hi[i]-e[i+ns]):7.2f}")
   print("Tramos")
   print("T, desde, hasta, V, Q, hf, hL, hT, S")
   for i in range(t):
       if "VR" in tp[i] or "VS" in tp[i] or "BO" in tp[i]:  # si hay un accesorio imprime la carga del accesorio
          hv =  f'{((A1[i,i]-A[i,i])*Qi[i]):.2f}'
          hv = "H"+ tp[i].strip() + "=" + hv
       else:
          hv=""
       print(f"{nt[i]:>3},{de[i]:>3}, {a[i]:>3}, {v[i]:6.2f}, {(Qi[i]*1000):6.2f}, {hf[i]:6.2f}, {hm[i]:6.2f}, {(hf[i]+hm[i]):6.2f}, {((hf[i]+hm[i])/l[i]):7.5f}, {hv}")
   print("timestamp, ",time.strftime("%c"))
   print("signature, crcs-2022")
#----------------------------------------------------------------------


#--- FIN DE FUNCIONES GLOBALES

"""
>>>> AQUI INICIA EL PROCESO DE CÁLCULO <<<<<
Si se trata de una ejecución en tiempo extendido, se inicia el contador "veces" y se ejecuta de acuerdo a la 
variable duración.   En cada caso se debe reiniciar los vectores qi y Ho
Se debe hacer vectores para salida extendida Qx, qfix, Hx, qix, Px

while veces < duracion:
"""

if modo == "-v":                                        # modo de impresión detallado
     print("----- INICIO DEL CÁLCULO -----")
     print("")
     print("----- Iteración inicial -----")
     # imprime las matrices iniciales
     io.imprime_matrices([N,q,Ho,qi*1000,B,C,Q*1000], ["N","q","Ho","qi","B","C","Q"] )
     print("")
     io.imprime_hid(nt, de, a, l, d, ks, km, tp, op, At, v, Re, f, hf, hm, alfa,t)
     print("")
     io.imprime_matrices([A,A1], ["A","A1"] )
     print("----Inician las iteraciones----")
     print("")

# Inicia el proceso de iteración
#-------------------------------
dqT, it = 1000, 0                                       # Se define dqT en 1000 e it en 0 para iniciar iteraciones
while dqT > imbalance and it < MaxIt:
  calcula_Hi_Qi()
  dq= np.subtract(Qi,Q)                                  # determina vector de desbalances de caudales en los nodos
  dqT= hid.calculaDesbalance(dq, n)
  #it = MaxIt                                            # esto es para hacer solo una iteración de prueba  >>>> COMENTAR
  it = it+1                                              # para hacer todas las iteraciones
  Q = Qi                                                 
  H = Hi
  qfi = hid.caudal_nudos_carga_fija(Q,nn,de,a,ns,t)      # calcula el caudal de los nudos de carga fija
  recalcular_alfa()                                      # con los nuevos Q vuelve a calcular v, Re, f, hf, hm y alfa
  A1= hid.construir_A1(alfa,Q,t,tp,op)                         # vuelve a reconstruir la matriz alfa [A']   
  A = hid.construir_A(A1,t,tp,op,e,de,a,hf,hm,H,Q,modo,ns)  # vuelve a reconstruir la matriz alfa [A]   
  if modo == "-v":       # modo de impresión detallado
     print("")
     print(f"-----Iteración número: {it:3} -----")
     print("")
     io.imprime_hid(nt, de, a, l, d, ks, km, tp, op, At, v, Re, f, hf, hm, alfa,t) 
     io.imprime_matrices([A,A1,qfi*1000,Hi,Qi*1000,dq] , ["A","A1","qfi","Hi","Qi","dq"] ) # imprime las matrices que cambian en cada iteración
     print("")
     print(f"-----Fin iteración: {it:>3}  Desbalance de caudales: {(1000*dqT):8.6F}")
     print("")
  if dqT < imbalance:
     if revisaChecks():
       dqT=1
       cierra_check()
       

  #fin del while
#----------

if modo == "-v":                                        # modo de impresión detallado
     print("----- FIN DEL CÁLCULO -----")
     print("")
     print("")
     imprime_reporte()

if dstn=="-f" and fmt=="-t" and modo=="-v":
   sys.stdout = orig_stdout 
   f_sal.close()



# ---> Una vez que converge el proceso de ieraciones, muestra los resultados
if modo=="-q":
    io.imprime_salida_quiet(Q,H,qfi,e,ns,fmt,dstn,fout)

if modo=="-n" and fmt=="-t":
   if dstn=="-f":
       fout_txt= fout.replace(".json",".txt")
       f_sal= open(fout_txt,"w")
       sys.stdout = f_sal 
       imprime_reporte()
       sys.stdout = orig_stdout 
       f_sal.close()
   else:
      imprime_reporte() 

if fmt=="-j" and modo=="-n":
    imprime_salida_json(fout)

if fmt=="-c" and modo=="-n":
   if dstn=="-f":
       fout_txt= fout.replace(".json",".csv")
       f_sal= open(fout_txt,"w")
       sys.stdout = f_sal 
       imprime_reporte_csv()
       sys.stdout = orig_stdout 
       f_sal.close()
   else:
       imprime_reporte_csv()
"""
   Aquí terminaría el while de veces
   se debe actualizar los vectores q, qi, qfi, Ho e insertar valores de Q,H, etc en los vectores x
"""
"""
    Copyright © 2022 Carlos Camacho Soto
    Publicado bajo licencia GPL v3.0
"""
# EOF ------