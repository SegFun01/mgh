""" Archivo con las funciones hidráulicas del método MGH
    Autor: Ing. Carlos Camacho Soto, ccamacho@segundafundacion.com
    Lugar: San José, Costa Rica
    Fecha: julio 2022
    f_hid.py: funciones hidráulicas 
    
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


def fCW(k, d, R, tol, ec): # parámetros de entrada ks/D, Re, t
   # primero se calcula f por S-W
   Re = pow(abs(R),0.9)
   f1 = 0.25 / ( math.log10(k/d/3.7 + 5.74/Re)**2)
   # print(f"f según Swamee-Jain: {f1:8.6f}")
   if ec=="C":
      # Calcular el factor de f por Colebrook-White
      f1= 0.01
      f=0
      dif = 0.1
      #it=0
      while dif>tol:
         f= ( 1 / ( -2* math.log10(k/d/3.7 + 2.51/(R * math.sqrt(f1) ) ) ))**2
         dif=abs(f1-f)
         f1=f
         # it=it+1
         # print(f"Iteracion:{it}   factor: {f:8.6f}")
   else:
      f=f1
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

def construir_A(a11,t,tp,op,e,de,a,hf,hm,H,Q,modo,ns):  
    # toma A1 y reemplaza alfa, beta y gama de acuerdo a [es] y [op]
    m = np.zeros([t,t],dtype=float) # aquí se guarda A1 temporalmente para ser devuelta
    for i in range(t):
       m[i,i]=a11[i,i]   #copia A1
    # Se necesitan los vectores e, de, a para computar el nuevo valor (a+b+c)
    for i in range(t):
         if tp[i].strip()=="VR":  # VALVULA REDUCTORA
              j=de[i]
              k=a[i]
              cota1 = e[j]
              cota2 = e[k]
              cota1 = (cota1 + cota2)/2
              LGHobj = cota1 + float(op[i])
              LGH1 = H[j-ns]
              LGHv = LGH1 - 0.5*(hm[i]+hf[i])
              g = LGHv-LGHobj
              if g<0:
                 g=0
              gQ = g / Q[i]
              m[i,i]=a11[i,i]+gQ
              #if modo=="2")   #revisar impresion
                #printf("Tramo %d, de %d a %d : VR, se ajusta A11[%d][%d] con &gamma;=%f, &gamma;/Q=%f, valor=%f<br>",$i+1, $j, $k, $i, $i,$g,$gQ,$A11[$i][$i]);          
         if tp[i].strip()=="VS":  # //VALVULA SOSTENEDORA
              j=de[i]
              k=a[i]
              cota1 = e[j]
              cota2 = e[k]
              cota1 = (cota1 + cota2)/2
              LGHobj = cota1 + float(op[i])
              LGH1 = H[j-ns]
              LGHv = LGH1 - 0.5*(hm[i]+hf[i])
              if LGHv < LGHobj: 
                  g = LGHobj-LGHv
              else: 
                 g = 0 
              gQ = g / Q[i]
              m[i,i]=a11[i,i] + gQ
              #if ($modo=="2"){
              #printf("En el tramo %d hay una VS, se ajusta A11[%d][%d] con &gamma;=%f, &gamma;/Q=%f, valor=%f<br>",$i+1, $j, $k, $i, $i,$g,$gQ,$A11[$i][$i]);
         if tp[i].strip()=="BO":  # BOMBA
             abc = op[i].split() 
             m[i,i]= a11[i,i]-(float(abc[0])*Q[i] + float(abc[1]) + float(abc[2])/Q[i]);
             # if ($modo=="2"){
             #  printf("En el tramo %d hay una BOMBA, se ajusta A11[%d][%d] con ALFA, BETA Y GAMA %f %f %f = %f<br>",$i+1, $i,$i, $abc[$pos-3],$abc[$pos-2],$abc[$pos-1],$A11[$i][$i]);
    return m         

def caudal_nudos_carga_fija(Q,nn,de,a,ns,t):
    qcf = np.zeros(ns,dtype=float)  # contendrá el valor del caudal de los nudos de carga fija tamaño [ns]
    for i in range(ns):
        for j in range(t):
            if de[j]==nn[i]:
                qcf[i]=qcf[i] - Q[j]
            if a[j]==nn[i]:
                qcf[i]=qcf[i] + Q[j]
    return qcf         

#### hasta aquí las funciones hidráulicas
