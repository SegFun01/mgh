# Pruebas en python con import funciones y variables
# Carlos Camacho Soto
# Fecha: julio 2022

#! /usr/bin/env python
"""
 Cálculo del tirante en canal abierto
 Determinar primero si es canal abierto o presión

  >> Condición 1: debe tener carga = 0 en el nudo de atrás
"""
import math
import sys

print("Determinar si es canal abierto o presión")
print("---")
d= float(input("Diámetro [mm]  : "))/1000
l= float(input("Longitud [m]   : "))
c1=float(input("Cota inicio [m]: "))
c2=float(input("Cota final [m] : "))
n= float(input("n de manning []: "))
q= float(input("Caudal [l/S]   : "))/1000
print("---")
a= math.pi * (d)**2 / 4
p= math.pi * d
r = a / p
h= c1 - c2
s = h / l

qmax= 1 / n * a * math.pow(r, (2/3)) * math.pow(s,(1/2))  

def calcula_theta():
  li = 0
  ls = math.pi * 2
  error=0.00001
  dif=1.0
  it=0
  AR23 = q * n / math.pow(s,0.5)
  print(f"AR23={AR23:7.4f}")
  print("  Theta    AR23   dif    Iter")
  while abs(dif)>error and it<50:
      m = (li+ls)/2
      f= ( d**2/8* ( m-math.sin(m) ) ) * math.pow( ( d/4*(1-math.sin(m) /m) ), (2/3) )
      dif= f - AR23
      if dif<0:
        li=m
      else:
        ls=m
      it=it+1
      print(f"{m:7.4} {f:7.4f} {dif:7.4f} {it}")
  return m

print(f"Caudal máximo:{qmax*1000:7.4f} [l/s]")
if qmax < (q):
   print("El tubo funciona a presión")
else:
   print("El tubo está a canal abierto...")
   print("Calculando tirante...")
   print("---")
   theta = calcula_theta() 
   y = d/2 * ( 1 - math.cos(theta/2))
   print(f"Tirante: {y*1000:7.4f} [mm]")


#EOF