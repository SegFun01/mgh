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

#---------->>>>>>>>>> Variables globales
fin = "input/default.mgh"
fout = fin + ".out"
titulo="Titulo de la red"
autor="Carlos Camacho Soto"
fecha="21/03/1966"
version="1.0.0"
viscosidad=1.007E-6
imbalance=1.0E-5
MaxIt=40
ns=1
n=5
t=7
factor=1
modo="-n"
ecuacion="S"        # Ecuación por defecto a usar Swamee-Jain, alternativa C=Colebrook-White
tol= 1E-6

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

#---------->>>>>>>>>> Carga de datos desde archivo
#-----Verificar los parámetros de entrada
if len(sys.argv) < 2 :   #cuando solo se escribe mgh, imprime el modo de uso y termina
   io.uso()
   fin = ".input/default.mgh"
   sys.exit()
else:                     #cuando se da el comando más un nombre de archivo, lo ejecuta en modo normal
   fin = sys.argv[1]
   fin = io.input_check(fin)
   fout = io.output_check(fin)
   #print(f"F input: {fin}   F output: {fout} ")
   modo = "-n"
if len(sys.argv) == 3 :  #se da comando, archivo, modo
   modo = sys.argv[2]
   modo.strip()
   if modo not in ["-n","-q","-v"]:
      modo="-n"
#antes de abrir archivo verificar si se desea incluir datos interactivamente
if "-i" in sys.argv:
    fin = io.crear_red()
    fout = io.output_check(fin)

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
titulo = f.readline().strip()
autor = f.readline().strip()
fecha = f.readline().strip()
version = f.readline().strip()
linea = f.readline()
valores = linea.split(",")
viscosidad = float(valores[0])
imbalance = float(valores[1])    
MaxIt = int(valores[2])
if valores[3].strip() in "C c":
    ecuacion="C"
linea = f.readline()
valores = linea.split(",")
ns = int(valores[0])          # nodos de carga fija NS
n = int(valores[1])           # nodos de demanda NN
t = int(valores[2])           # numero de tramos NT
factor = float(valores[3])    # factor de demanda de todos los nudos   
#-----Lee los nudos de carga fija
for i in range(0,ns):
   linea = f.readline()
   valores = linea.split(",")
   nn.append(int(valores[0]))
   e.append(float(valores[1]))
   #trash = valores[2].split(" ")
   q.append(float(valores[2]))          # este q es la carga de los nudos de carga fija. Usar más adelante para guardar q de los tanques
   h.append(float(valores[2]))          # copiando la altura en el vector h también  REVISAR ESTO PARA USAR SOLO H, ahora no es posible
   fi.append(0)
#-----Leer los nudos de demanda
for i in range(0,n):
   linea = f.readline()
   valores = linea.split(",")
   #trash = valores[2]
   nn.append(int(valores[0]))
   e.append(float(valores[1]))
   q.append(float(valores[2]))
   fi.append(float(valores[3]))
#-----Leer los datos de los tramos
for i in range(0,t):
   linea = f.readline()
   valores = linea.split(",")
   nt.append(int(valores[0]))
   de.append(int(valores[1]))
   a.append(int(valores[2]))
   l.append(float(valores[3]))    
   d.append(float(valores[4]))        
   ks.append(float(valores[5]))    
   km.append(float(valores[6]))    
   es.append(valores[7])    
   op.append(valores[8].strip())
f.close()  

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
#---------->>>>>>>>>> Iniciar matrices: carga de los datos en las matrices a partir de los vectores de lectura
Q.fill(0.1)                          # iniciar caudales en tramos
np.fill_diagonal(N,2)                # iniciar matriz N con 2 en la diagonal
for i in range(0,ns):                
    Ho[i]=(h[i])                     # iniciar matriz alturas fijas 
for i in range(ns,n+ns):
    qi[i-ns]=(q[i]/1000*factor*fi[i]) # iniciar matriz demandas en nudos   
for i in range(t):
    for j in range(ns):
        if de[i]==j and es[i]!="TC":
            C[i,j]=-1                  # iniciar matriz topológica de cargas fijas nudo de salida=-1
        if a[i]==j and es[i]!="TC":
            C[i,j]=1                   # iniciar matriz topológica de cargas fijas nudo de llegada =-1
    for j in range(ns,ns+n):
        jj=j-ns
        if de[i]==j:
            B[i,jj]= -1.0            # iniciar matriz topológica nudo-tramo
        if a[i]==j:
            B[i,jj]= 1.0              
    At[i]=hid.area(d[i])             # iniciar matriz Areas de Tubos
    v[i]=hid.ve(Q[i],At[i])          # iniciar matriz de velocidades en tubos
    Re[i]=hid.reynolds(v[i],d[i],viscosidad) # iniciar matriz Reynolds
    if ecuacion=="C":
        f[i]= hid.fCW(ks[i],d[i],Re[i],tol)    # iniciar matriz factor fricción usando Colebrook-White
    else:
        f[i]=hid.fSJ(ks[i],d[i],Re[i])       # iniciar matriz factor fricción usando Swamee-Jain
    hf[i]=hid.hfr(f[i],l[i],v[i],d[i])       # iniciar matriz pérdidas fricción
    hm[i]=hid.hme(km[i],v[i])                # iniciar matriz pérdidas locales 
    alfa[i]=hid.alf(hf[i]+hm[i],Q[i])        # Iniciar matriz de alfas
BT = np.transpose(B)                         # iniciar matriz B transpuesta
A1= hid.construir_A1(alfa,Q,t)               #iniciar matriz A'
A = hid.construir_A(A1,t,es,op,e,de,a,hf,hm,H,Q,modo) # iniciar matriz A       

#---------->>>>>>>>>> Check de matrices:   comentar
#io.matrices_check(Ho,qi,H,Q,B,BT,C,I,N,At,v,Re,f,hf,hm,alfa,A,A1)


#---> DEFINICION DE FUNCIONES GOLABLES --------------------------------

#---> RECALCULAR las matrices v, Re, f, hf, hm para obtener el alfa en cada iteración
def recalcular_alfa():
   global v,Re,f,hf,hm,alfa
   for i in range(t):
       v[i]= hid.ve(Q[i],At[i])
       Re[i]=hid.reynolds(v[i],d[i],viscosidad)
       if ecuacion=="C":
          f[i]= hid.fCW(ks[i],d[i],Re[i],tol)        # f usando Colebrook-White
       else:   
          f[i]= hid.fSJ(ks[i],d[i],Re[i])          # f usando Swamee-Jain
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

#---> Impresión de reporte final
def imprime_reporte():                       # pasar a f_io con valores de entrada 
   print("MÉTODO DEL GRADIENTE HIDRÁULICO              v1.0.0-alpha")
   print("")
   print("Archivo de entrada:", fin)
   print("Titulo:     ",titulo)
   print("Autor:      ",autor)
   print("Fecha:      ",fecha)
   print("Versión:    ",version)
   print("Viscosidad:",viscosidad)
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
      print(f"{nn[i+ns]:>3}  {e[i+ns]:7.2f}    {q[i+ns]:7.2f}   {fi[i+ns]:6.2f} ")
   print("---------------------------------")
   print("")
   print("Tramos")
   print("  T   de->a      L     D     A       ks     kL   Estado   Op ")
   print("---------------------------------------------------------------")
   for i in range(t):
      print(f"{nt[i]:>3}  {de[i]:>3}{a[i]:>3} {l[i]:7.0f} {d[i]:5.0f} {At[i]:7.4f}  {ks[i]:5.4f} {km[i]:5.1f}   {es[i]:>3}   {op[i]} ")
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
   print("  N  Elevación   Q Base    FVH   Q Neto     Carga   Presión")
   print("-----------------------------------------------------------")
   for i in range(n):
       print(f"{nn[i+ns]:>3}  {e[i+ns]:7.2f}    {q[i+ns]:7.2f}  {fi[i+ns]:6.2f}  {(qi[i]*1000):6.2f}    {H[i]:6.2f}  {(Hi[i]-e[i]):7.2f}")
   print("-----------------------------------------------------------")
   print("")
   print("Tramos")
   print("  T   de->a      V       Q       hf      hL      hT       S")
   print("--------------------------------------------------------------")    
   for i in range(t):
       print(f"{nt[i]:>3}  {de[i]:>3}{a[i]:>3}   {v[i]:6.2f}  {(Qi[i]*1000):6.2f}  {hf[i]:6.2f}  {hm[i]:6.2f}  {(hf[i]+hm[i]):6.2f}   {((hf[i]+hm[i])/l[i]):7.5f}")
   print("--------------------------------------------------------------")    
   print("")
   print("Fecha y hora de esta corrida: ",time.strftime("%c"))
   print("crcs-2022")
#----------------------------------------------------------------------

#--- FIN DE FUNCIONES GLOBALES

if modo == "-v":                                        # modo de impresión detallado
     print("----- INICIO DEL CÁLCULO -----")
     print("")
     print("----- Iteración inicial -----")
     # imprime las matrices iniciales
     io.imprime_matrices([q,Ho,qi,B,C,Q], ["q","Ho","qi","B","C","Q"] )
     print("")
     io.imprime_hid(nt, de, a, l, d, ks, km, es, op, At, v, Re, f, hf, hm, alfa,t)
     print("")
     io.imprime_matrices([A,A1], ["A","A1"] )
     print("----Inician las iteraciones----")
     print("")

# Inicia el proceso de iteración
#-------------------------------
dqT, it = 1000, 0                                        # Se define dqT en 1000 e it en 0 para iniciar iteraciones
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
  A1= hid.construir_A1(alfa,Q,t)                         # vuelve a reconstruir la matriz alfa [A']   
  A = hid.construir_A(A1,t,es,op,e,de,a,hf,hm,H,Q,modo)  # vuelve a reconstruir la matriz alfa [A]   
  if modo == "-v":       # modo de impresión detallado
     print("")
     print(f"-----Iteración número: {it:3} -----")
     print("")
     io.imprime_hid(nt, de, a, l, d, ks, km, es, op, At, v, Re, f, hf, hm, alfa,t) 
     io.imprime_matrices([A,A1,qfi,Hi,Qi,dq] , ["A","A1","qfi","Hi","Qi","dq"] ) # imprime las matrices que cambian en cada iteración
     print("")
     print(f"-----Fin iteración: {it:>3}  Desbalance de caudales: {(1000*dqT):8.6F}")
     print("")
  #fin del while
#----------

if modo == "-v":                                        # modo de impresión detallado
     print("----- FIN DEL CÁLCULO -----")
     print("")
     print("")

# ---> Una vez que converge el proceso de ieraciones, muestra los resultados
if modo=="-q":
    io.imprime_salida_quiet(Q,H,e,ns)
else:
    imprime_reporte()

"""
    Copyright © 2022 Carlos Camacho Soto
    Publicado bajo licencia GPL v3.0
"""
# EOF ------