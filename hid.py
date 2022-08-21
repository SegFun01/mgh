#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Modelado de redes hidráulicas por el método del gradiente hidráulico
# Autor: Ing. Carlos Camacho Soto
# Fecha: 07 de febrero de 2019
# Versión: 1.0
# Funciones hidráulicas

import math
import sys
import numpy as np

# Funciones hidráulicas ----------
def calculaDesbalance(Q, q, t):
    #Calcula el máximo desbalance de caudales (revisar si se requiere deltaQ)
    des = 0
    for i in range(t):
        if  abs(q[i]-Q[i]) > des:
            des = abs(q[i]-Q[i])
    return des        
        
def area(D):
    """Calcula el area de la tuberia en m2 con diametro en mm"""
    a = D * D * math.pi / 4 / 1000 / 1000
    return a
    
def ve(q,a):
    """ Calcula la velocidad del flujo a partir del cauda y el area [m3/s] y [m2]"""
    v = q / a
    return v

def reynolds(v,d,vis):
    """Calcula el numero de reynolds para la condicion de flujo dada, diámetro en mm"""
    re = abs( v * d / 1000 / vis )
    return re

def fSJ(k, d, R):
    """Calcula el factor de friccion con Swamee Jain con k y d en mm"""
    Re = pow(abs(R),0.9)
    f = 0.25 / ( math.log10(k/d/3.7 + 5.7/Re)**2)
    return f

def hfr(f,L,v,d):
    """Calcula las perdidas por friccion en un tramo """
    h = f * L * (v**2) / (d/1000) / 19.62
    return h
    
def hme(km, v):
    """Calcula las perdidas locales de un tramo """
    h = km * (v**2) / 19.62
    return h
    
def alf(h,q):
   """Calcula el valor alfa para cada tramo con datos de perdidas"""
   q = float(abs(q))
   a = h / (q**2)
   return a