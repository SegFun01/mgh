# f_HQ_solver.py
# Algoritmo de solución de las matrices [Hi] y [Qi]
#
import math
import numpy as np

from mgh import Q, H, Ho, B, BT, C, N, I, A, A1, Qi, Hi, qi

def calcula_Hi_Qi():
   #----------->>>>>>>>>> Deficinicón de variables globales
   global Q, H, Ho, B, BT, C, N, I, A, A1, Qi, Hi
   #----------->>>>>>>>>> Variables locales M1, M2, M3, M4 y M5
   # - paso 1 
   M3= np.matmul(N,A1)
   M4= np.matmul(A,Q)
   M5= np.matmul(C,Ho)
   # - paso 2
   M1= np.matmul(BT,M3)
   M4= np.matmul(C,Ho)
   # - paso 3
   M1= np.matmul(M1,B)
   M3= np.linalg.inv(M3)
   # - paso 4
   M1= np.linalg.inv(M1)
   M2= np.matmul(BT,M3)
   # - paso 5
   M1= M1*(-1)
   M2= np.matmul(M2,M4)
   # - paso 6
   M4= np.matmul(BT,Q)
   # - paso 7
   M4= np.subtract(M4,qi)
   # - paso 8
   M2= np.subtract(M2,M4)
   # - paso 9
   Hi = np.matmul(M1,M2)  # primer resultado
   # - paso 10
   M1= np.subtract(I,M3)
   M4= np.matmul(B,Hi)
   # - paso 11
   M1= np.subtract(M1,A)
   M4= np.add(M4,M5)
   # - paso 12
   M1= np.matmul(M1,Q)
   M2= np.matmul(M3,M4)
   # - paso 13
   Qi= np.subtract(M1,M2) # segundo resultado
#------------