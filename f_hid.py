# Archivo con las funciones hidráulicas del método MGH
# Carlos Camacho Agosto 2022
# f_hid.py: funciones hidráulicas 
#---
 
import math
import numpy as np

#---> Calcula el MAYOR desbalance de caudales en cada iteración de todos los nudos
def calculaDesbalance(dq, t):
    des = 0
    for i in range(t):
        if  abs(dq[i]) > des:
            des = abs(dq[i])      #¿esto debe ser en valor absoluto? -> no importa, se usa como criterio de fin
    return des        

#---> Calcula el area de la tuberia en m2 con diametro en mm        
def area(D):
    a = D * D * math.pi / 4 / 1000 / 1000
    return a
    
#---> Calcula la velocidad del flujo a partir del caudal y el area    
def ve(q,a):
    v = q / a
    return v

#---> Calcula el numero de reynolds para la condicion de flujo dada
def reynolds(v,d,vis):
    re = abs( v * d / 1000 / vis )
    return re

#---< Calcula el factor de friccion con Swamee Jain, se puede mejorar con Colebrook White
def fSJ(k, d, R):
    Re = pow(abs(R),0.9)
    f = 0.25 / ( math.log10(k/d/3.7 + 5.74/Re)**2)
    return f

#---< Calcula el factor de friccion con Colebrook White
def fCW(k, d, R, t): # parámetros de entrada ks/D, Re, t
   # Calcular el factor de f por Colebrook-White
   f1= 0.01
   f=0
   dif = 0.1
   #it=0
   while dif>t:
      f= ( 1 / ( -2* math.log10(k/d/3.7 + 2.51/(R * math.sqrt(f1) ) ) ))**2
      dif=abs(f1-f)
      f1=f
      #it=it+1
      #print("Iteracion:",it, " factor: ",f)
   return f

#---> Calcula las perdidas por friccion en un tramo
def hfr(f,L,v,d):
    h = f * L * (v**2) / (d/1000) / 19.62
    return h

#---> Calcula las perdidas locales de un tramo    
def hme(km, v):
    h = km * (v**2) / 19.62
    return h
    
#--->Calcula el valor de alfa dividiendo h entre el caudal al cuadrado
def alf(h,q):
   q = float(abs(q))
   a = h / (q**2)
   return a
    

# al parecer esta función reA11 no va a ser necesaria porque se usan Construir_A11I y Consrtuir_A11 ?????       
def reA11(a,q,t):
    #Reescribe la matriz alfa con valores de cada iteracion
    mat = []
    for i in range(t):
        mat.append([])
        for j in range(t):
            if i==j:
                mat[i].append(a[i]*q[i])
            else :
                mat[i].append(0)  
    return mat
    
##### estas funciones están en edición
def construir_A1(alfa,q,t):
   # devuelve una nueva matriz A11I -> sin los valores beta y gama
   m=np.zeros([t,t],dtype=float)
   for i in range(t):
       m[i,i]=alfa[i]*q[i]
       #print("m[i,i],alfa[i],Q[i] ",m[i,i],alfa[i],q[i])
   return m

def construir_A(a11,t,es,op,e,de,a,hf,hm,H,Q,modo):  
    # toma A1 y reemplaza alfa, beta y gama de acuerdo a [es] y [op]
    m = np.zeros([t,t],dtype=float) # aquí se guarda A1 temporalmente para ser devuelta
    for i in range(t):
       m[i,i]=a11[i,i]   #copia A1
    # Se necesitan los vectores e, de, a para computar el nuevo valor (a+b+c)
    for i in range(t):
         if es[i].strip()=="VR":  # VALVULA REDUCTORA
              j=de[i]
              k=a[i]
              cota1 = e[j]
              cota2 = e[k]
              cota1 = (cota1 + cota2)/2
              LGHobj = cota1 + float(op[i])
              LGH1 = H[j]
              LGHv = LGH1 - 0.5*(hm[i]+hf[i])
              g = LGHv-LGHobj
              if g<0:
                 g=0
              gQ = g / Q[i]
              m[i,i]=a11[i,i]+gQ
              #if modo=="2")   #revisar impresion
                #printf("Tramo %d, de %d a %d : VR, se ajusta A11[%d][%d] con &gamma;=%f, &gamma;/Q=%f, valor=%f<br>",$i+1, $j, $k, $i, $i,$g,$gQ,$A11[$i][$i]);          
         if es[i].strip()=="VS":  # //VALVULA SOSTENEDORA
              j=de[i]
              k=a[i]
              cota1 = e[j]
              cota2 = e[k]
              cota1 = (cota1 + cota2)/2
              LGHobj = cota1 + op[i]
              LGH1 = H[j]
              LGHv = LGH1 - 0.5*(hm[i]+hf[i])
              if LGHv < LGHobj: 
                  g = LGHobj-LGHv
              else: 
                 q = 0 
              gQ = g / Q[i]
              m[i,i]=a11[i,i] + gQ
              #if ($modo=="2"){
              #printf("En el tramo %d hay una VS, se ajusta A11[%d][%d] con &gamma;=%f, &gamma;/Q=%f, valor=%f<br>",$i+1, $j, $k, $i, $i,$g,$gQ,$A11[$i][$i]);
         if es[i].strip()=="BO":  # BOMBA
             abc = op[i].split() 
             m[i,i]= a11[i,i]-(float(abc[0])*Q[i] + float(abc[1]) + float(abc[2])/Q[i]);
             # if ($modo=="2"){
             #  printf("En el tramo %d hay una BOMBA, se ajusta A11[%d][%d] con ALFA, BETA Y GAMA %f %f %f = %f<br>",$i+1, $i,$i, $abc[$pos-3],$abc[$pos-2],$abc[$pos-1],$A11[$i][$i]);
    return m         

def caudal_nudos_carga_fija(Q,nn,de,a,ns,t):
    qcf = np.zeros(ns,dtype=float)  # contendrá el valor del caudal de los nudos de carga fija tamaño [ns]
    for i in ns:
        for j in t:
            if de[j]==nn[j]:
                qcf[i]=qcf[i] - Q[j]
            if a[j]==nn[j]:
                qcf[i]=qcf[i] + Q[j]
    return qncf         

#### hasta aquí las funciones hidráulicas
