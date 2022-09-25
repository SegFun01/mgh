"""  
 * Leer los datos de las curvas y usarlos para calcular caudales
   El loop realiza el cálculo de los caudales de cada iteración usando la curva
   y debe calcular en nuevo nivel de tanque.
 TODO: falta calcular el nivel.
 TODO: falta que el loop sea usado en el programa principal
 * Con cada iteración se deben guardar los valores de cada iteración de Q, H, P, qif
 * para pasarlos a cada tramo 
"""

import json
import random

duracion=24
hora=8
dow=3
mes=3
curvas=[]
q0=[10.0,15.0,10.0,15.0,10.0,15.0]
qi=[10.0,15.0,10.0,15.0,10.0,15.0]
Q=[]
H=[]
Qx=[]
Hx=[]
Px=[]
qfix=[]

def get_curva():
    m_curva=[]
    with open('./input/curvas.json','r') as curvas:
       j_curvas = json.load(curvas)
    d_curvas=j_curvas.get('curvas')
    for i in d_curvas.keys(): 
      x=d_curvas.get(i)  
      m_curva.append(x)
    return m_curva
    
curvas=get_curva()

for i in range(duracion):      # esto se realiza las veces requeridas en el periodo extendido
   fvh = curvas[0][hora]
   fdow = curvas[4][dow]
   fm = curvas[5][mes]
   for j in range(len(q0)):
      qi[j]=round(fvh*fdow*fm*q0[j],2)   #? en la ejecución real mejor no redondear por la pérdida de presición en cada iteración
      Q.append(round((qi[j])**2*random.random(),2))
      H.append(round(Q[j]**0.5,2))
   Qx.append(Q)
   Hx.append(H)
   Q=[]
   H=[]
   #TODO: hay que calcular el nuevo nivel (carga) de los nudos de carga fija
   #TODO: con las demandas calculadas se puede hacer la corrida i
   #! print(f"{i} hora:{hora} dow:{dow} fvh:{fvh} fdow:{fdow} fvm:{fm} q:{qi}")
   hora = (hora + 1) % 24
   if hora==0:
      dow = (dow +1) % 7    
print("---")
print(f"{Qx}")
print("---")
print(f"{Hx}")
for j in range(len(q0)):
   print(f"Nudo {j}----------")
   for i in range(duracion):
      print(f"Hora: {i}  Caudal: {Qx[i][j]}  Carga: {Hx[i][j]}")


   
   
   