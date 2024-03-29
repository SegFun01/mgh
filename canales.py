# Cálculo de tirante crítico y tirante normal en canales
# trapezoidales y circulares
# ------------------------------------------------------
# Carlos Camacho Soto
# Fecha: noviembre 2023

#! /usr/bin/env python

import math
import sys
PI = math.pi

# Funciones de y para usar en método de Newton-Raphson
def funcion_ycT(b,z,y,q):
  y1=((b*y+z*(y**2))**1.5)/((b+2*z*y)**0.5)-q/(9.81**0.5)
  return y1
  
def funcion_ynT(b,z,y,q,n,S):
  y1=((b*y+z*(y**2))**(5/3))/((b+2*y*(1+z**2)**0.5)**(2/3))-q*n/(S**0.5)
  return y1

def funcion_ycC(d,O,q):
  O1= ((1/8*(O-math.sin(O)) )**1.5) / ((math.sin(O/2) )**0.5) * (d**2.5) - (q /(9.81**0.5))
  return O1
  
def funcion_ynC(d,O,q,n,S):
  O1= (d**(8/3)) * ((1/8*(O-math.sin(O)))**(5/3)) / ((O/2)**(2/3)) - (q*n/(S**0.5))
  return O1

# Método de Newton-Raphson para y crítica en canal trapezoidal
def ycriticaT(q,b,z):
  h=0.000001
  y0=b/2
  y1=b/2
  dif=1.0
  it=0
  error=0.000001  
  while dif>error and it<50:
      fy=funcion_ycT(b,z,y0,q)
      fyh=funcion_ycT(b,z,y0+h,q)
      y1= y0 -(fy*h)/(fyh-fy)
      dif=abs(y1-y0)
      it=it+1
      y0 = y1
  return y1

# Método de Newton-Raphson para y normal en canal trapezoidal
def ynormalT(q,b,z,n,S):
  h=0.000001
  y0=b/2
  y1=b/2
  dif=1.0
  it=0
  error=0.000001  
  while dif>error and it<50:
      fy=funcion_ynT(b,z,y0,q,n,S)
      fyh=funcion_ynT(b,z,y0+h,q,n,S)
      y1= y0 -(fy*h)/(fyh-fy)
      dif=abs(y1-y0)
      it=it+1
      y0 = y1
  return y1

# Método de Newton-Raphson para y crítica en canal circular
def ycriticaC(q,d):
  h=0.000001
  y0=PI
  y1=PI
  dif=1.0
  it=0
  error=0.000001  
  while dif>error and it<50:
      fy=funcion_ycC(d,y0,q)
      fyh=funcion_ycC(d,y0+h,q)
      y1= y0 -(fy*h)/(fyh-fy)
      dif=abs(y1-y0)
      it=it+1
      y0 = y1
  y1= d/2*(1+math.cos(PI-y1/2))
  return y1

# Método de Newton-Raphson para y normal en canal circular
def ynormalC(q,d,n,S):
  h=0.000001
  y0=PI
  y1=PI
  dif=1.0
  it=0
  error=0.000001  
  while dif>error and it<50:
      fy=funcion_ynC(d,y0,q,n,S)
      fyh=funcion_ynC(d,y0+h,q,n,S)
      y1= y0 -(fy*h)/(fyh-fy)
      dif=abs(y1-y0)
      it=it+1
      y0 = y1
  y1= d/2*(1+math.cos(PI-y1/2))
  return y1

  
# Cuerpo del programa
print("---------------------------------------")
print("     Cálculo de yCrítica y yNormal")
print("---------------------------------------")
print("Tipo de canal: ")
tipo=input("T/t= Trapezoidal C/c=Circular : ? ")
print("---------------------------------------")
if tipo.lower()=="c" :
  print(">>>>>>>> Canal Circular <<<<<<<<")
  q= float(input("Caudal [m3/s]  : "))
  d= float(input("Diámetro [m]   : "))
  n= float(input("n de Manning   : "))
  S= float(input("Pendiente [m/m]: "))
  print("------------------------------------")
  print(f"y Crítica [m] : {ycriticaC(q,d)}")
  print(f"y Normal [m]  : {ynormalC(q,d,n,S)}")
  print("------------------------------------")  
else : 
  print(">>>>>>> Canal Trapezoidal <<<<<<<")
  q= float(input("Caudal [m3/s]  : "))
  b= float(input("Ancho (b) [m]  : "))
  z= float(input("Talud (Z)      : "))
  n= float(input("n de Manning   : "))
  S= float(input("Pendiente [m/m]: "))
  print("---------------------------------------")
  print(f"y Crítica [m] : {ycriticaT(q,b,z)}")
  print(f"y Normal [m]  : {ynormalT(q,b,z,n,S)}")

print("---------------------------------------")

#EOF  crcs2023