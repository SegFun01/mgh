# Modelado de redes hidraulicas por el metodo del gradiente hidraulico
# Autor: Ing. Carlos Camacho Soto
# Fecha: julio 2022
#! /usr/bin/env python

#---------->>>>>>>>>> Importar archivos y librerías
import math
import sys
import numpy as np
import f_hid as hid
import f_io as io
import f_HQ_solver as hq

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

#---------->>>>>>>>> Definicion de vectores globales para cargar los datos desde el archivo
nn= []   # id de los nudos
e = []   # elevaciones de cada nudo
q = []   # demandas de los nudos
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

#---------->>>>>>>>>> Definicion de matrices globales del MGH
qi = np.zeros(n,dtype=float)       # caudales demandados en los nodos
Ho = np.zeros(ns,dtype=float)      # cargas fijas
H = np.zeros(n,dtype=float)        # cargas dinamicas en los nudos
C = np.zeros([t,ns],dtype=float)   # topologia tramos x nudos de carga fija [t x ns]
B = np.zeros([t,n],dtype=float)    # topologia nudo a tramo  [t x n]
BT= np.zeros([n,t],dtype=float)    # transpuesta de B [n x t] esta matriz no se requiere
A1= np.zeros([t,t],dtype=float)    # matriz de valores Alfa de modo que hf=alfa*Q  ->A11'
A = np.zeros([t,t],dtype=float)    # matriz de valores Alfa para accesorios especiales (bomba y válvula)
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

#---------->>>>>>> Leer parametros de entrada, archivo y rellenar vectores
io.cargar_desde_archivo(sys.argv)

#---------->>>>>>>>>> Iniciar matrices: carga de los datos en las matrices a partir de los vectores de lectura
io.iniciar_matrices()

#---------->>>>>>>>>> Revisar topología de la red
io.revisar_topologia()

#---------->>>>>>>>>> Iniciar matrices [A] y [A'] de valores alfa
A1= hid.construir_A1(alfa,Q,t)
A = hid.construir_A(A1,t,es,op,e,de,a,hf,hm,H,Q,modo)         

#---------->>>>>>>>>> Imprimir un checkeo de las matrices (TEMPORALMENTE)
io.matrices_check()                                      # este chequeo es temporal, removerlo cuando se revisen las matrices

# Inicia el proceso de iteración
#-------------------------------
dqT, it = 1000, 0                                        # Se define dqT en 1000 e it en 0 para iniciar iteraciones
while dqT > imbalance and it < MaxIt:
  hq.calcula_Hi_Qi()
  dq= np.subtract(np.matmul(BT,Qi),qi)
  dqT= hid.calculaDesbalance(dq, t)
  it = MaxIt                                             # esto es para hacer solo una iteración de prueba  >>>> COMENTAR
  #it = it+1                                              # para hacer todas las iteraciones
  Q= Qi
  H= Hi
  io.recalcular_alfas()                                  # con los nuevos Q vuelve a calcular v, Re, f, hf, hm y alfa
  A1= hid.construir_A1(alfa,Q,t)                         # vuelve a reconstruir la matriz alfa [A']   
  A = hid.construir_A(A1,t,es,op,e,de,a,hf,hm,H,Q,modo)  # vuelve a reconstruir la matriz alfa [A]
  #fin del while
#----------

#io.imprime_salida_normal() / io.imprimesalida_quiet
#EOF