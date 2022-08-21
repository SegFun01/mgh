# Modelado de redes hidraulicas por el metodo del gradiente hidraulico
# Autor: Ing. Carlos Camacho Soto
# Fecha: julio 2022
#! /usr/bin/env python

# Importar archivos y librerías
# -----------------------------
import math
import sys
import numpy as np
import f_hid as hid
import f_io as io

# Definicion de vectores globales para cargar los datos desde el archivo
# ----------------------------------------------------------------------
nn= []  # id de los nudos
e= []   # elevaciones de cada nudo
q= []   # demandas de los nudos
nt = [] # id de los tramos o tubos
de= []  # id del nudo de inicio del tramo
a= []   # id del nudo final del tramo
l= []   # longitudes de cada tramo en [m]
d= []   # diametro de cada tramo en [mm]
ks= []  # coeficiente de rugosidad del tra¿mo en [mm]
km= []  # coeficiente de perdidas locales del tramo
es= []  # estado del tramo: TA abierto, TC cerrado, BO bomba, VRP válvula, etc
tmp= [] # temporal para guardar valores de las opciones del tramo
op=[]   # opciones del tramo: presión de ajuste, alfa,beta,gama de la bomba

# Leer parametros de entrada, archivo y rellenar vectores
# ------------------------------------------------------
# TODO lo referente a leer del archivo y cargarlo en 
# los vectores se puede transferir a una función en f_io.py
#
if len(sys.argv) < 2 : 
    io.uso()
    fin = "default.mgh"
    sys.exit()
else: 
    fin = sys.argv[1]
    fout = fin + ".out"
    modo = "-n"
if len(sys.argv) == 3 : 
    modo = sys.argv[2]
    modo.strip()
f = open(fin,'r')
titulo = f.readline().strip()
autor = f.readline().strip()
fecha = f.readline().strip()
version = f.readline().strip()
linea = f.readline()
valores = linea.split(",")
viscosidad = float(valores[0])
imbalance = float(valores[1])    
MaxIt = int(valores[2])
linea = f.readline()
valores = linea.split(",")
ns = int(valores[0])          # nodos de carga fija NS
n = int(valores[1])           # nodos de demanda NN
t = int(valores[2])           # numero de tramos NT
factor = float(valores[3])    # factor de demanda de todos los nudos

#lee los nudos de carga fija
#---------------------------
for i in range(0,ns):
    linea = f.readline()
    valores = linea.split(",")
    nn.append(int(valores[0]))
    e.append(float(valores[1]))
    trash = valores[2].split(" ")
    q.append(float(trash[1]))

# Leer los nudos de demanda
# -------------------------
for i in range(0,n):
    linea = f.readline()
    valores = linea.split(",")
    #trash = valores[2]
    nn.append(int(valores[0]))
    e.append(float(valores[1]))
    q.append(float(valores[2]))

# Leer los datos de los tramos
# ----------------------------
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
  

# Definicion de matrices del MGH
#----------------------------------
qi = np.zeros(n,dtype=float)       # caudales demandados en los nodos
Ho = np.zeros(ns,dtype=float)      # cargas fijas
H = np.zeros(n,dtype=float)        # cargas dinamicas en los nudos
A10 = np.zeros([t,ns],dtype=float) # topologia tramos x nudos de carga fija [t x ns]
A12 = np.zeros([t,n],dtype=float)  # topologia nudo a tramo  [t x n]
# A21 = []                         # transpuesta de A12 [n x t] esta matriz no se requiere
A11I = np.zeros([t,t],dtype=float) # matriz de valores Alfa de modo que hf=alfa*Q  ->A11'
A11 =np.zeros([t,t],dtype=float)   # matriz de valores Alfa para accesorios especiales (bomba y válvula)
I = np.identity(t,dtype=float)     # matriz identidad [t x t]
N = np.zeros([t,t],dtype=float)    # exponentes de la ecuación de pérdidas, 2 en Darcy Weisbach
Q=np.zeros([t],dtype=float)        # caudales en los tramos [m3/s]
A=np.zeros([t],dtype=float)        # áreas de las tuiberías en [m2]
v=np.zeros([t],dtype=float)        # velocidades del flujo en los tubos [m/s]
Re=np.zeros([t],dtype=float)       # números de Reynolds ern los tramos
f=np.zeros([t],dtype=float)        # factores de fricción de D-W de cada tramo
hf=np.zeros([t],dtype=float)       # pérdidas por fricción de cada tramo en [m]
hm=np.zeros([t],dtype=float)       # pérdidas locales de cada tramo en [m]
alfa=np.zeros([t],dtype=float)     # valores alfa de cada tramo
beta=np.zeros([t],dtype=float)     # valores beta de cada tramo para usar en A11
gama=np.zeros([t],dtype=float)     # valores gama de cada tramo para usar en A11

# Carga de los datos en las matrices a partir de los vectores de lectura
# ---------------------------------------------------------------------
# Nota: esto se podría poner en una función en f_io.py
#
Q.fill(0.1)
np.fill_diagonal(N,2)
for i in range(0,ns):   
    Ho[i]=(q[i]) 
for i in range(ns,n+ns):
    qi[i-ns]=(q[i]/1000*factor)  
for i in range(t):
    for j in range(ns):
        if de[i]==j or a[i]==j:
            A10[i]=-1
    for j in range(ns,ns+n):
        jj=j-ns
        if de[i]==j:
            A12[i,jj]= -1.0
        if a[i]==j:
            A12[i,jj]= 1.0 
    A[i]=hid.area(d[i])
    v[i]=hid.ve(Q[i],A[i])
    Re[i]=hid.reynolds(v[i],d[i],viscosidad)
    f[i]=hid.fSJ(ks[i],d[i],Re[i])
    hf[i]=hid.hfr(f[i], l[i], v[i], d[i]) 
    hm[i]=hid.hme(km[i],v[i])
    alfa[i]=hid.alf(hf[i]+hm[i],Q[i])
    A11[i,i]=alfa[i]*Q[i]  # falta considerar beta & gama
    A11I[i,i]=alfa[i]*Q[i] 

# Revisión de la topología de nudo a tramo
# Se debe asegurar que todos los nodos estén conectados
# Esto se puede pasar a una función en f_io.py
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
#print("Topología de nudos OK")
         
# Recordar hacer funciones de impresión en f_io.py
# ------------------------------------------------
# 
# Imprimir matrices para verificación
# -----------------------------------
print("Archivo de salida:" , fout)
print("Archivo de entrada:", fin)
print("Modo de ejecución: ", modo)
print("Titulo:     ",titulo)
print("Autor:      ",autor)
print("Fecha:      ",fecha)
print("Versión:    ",version)
print("Viscosidad: ",viscosidad)
print("Imbalance:  ",imbalance)
print("Máx iter:   ",MaxIt)
print("Nodos carga fija: ",ns)
print("Nodos de demanda: ",n)
print("Tramos o tubos:   ",t)
print("Factor de demanda:",factor)
print("Matriz cargas fijas:",Ho) 
print("Matriz demandas:",qi) 
print("Matriz de cargas en nudos:",H)
print("Topología nudos de carga fija: A10")
print(A10)
print("A12")
print(A12)
print("A21")
print(A12.transpose())
print("I")
print(I)
print("N")
print(N)
print("Q")
print(Q)
print("A")
print(A)
print("v")
print(v)
print("Re")
print(Re)
print("f")
print(f)
print("hf")
print(hf)
print("hm")
print(hm)
print("alfa")
print(alfa)
print("A11")
print(A11)

# Inicia el proceso de iteración
#-------------------------------
dq, it = 1000, 0                      # Se denine dq en 100 e it en 0 para iniciar iteraciones
while dq > imbalance and it < MaxIt:
  NA11I= np.matmul(N,A11I)
  print("NA11I")
  print(NA11I)
  # se deben procesar las matrices...
  it = MaxIt  # esto es para hacer solo una iteración de prueba

#EOF