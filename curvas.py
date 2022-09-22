###### leer los datos de las curvas y usarlos para calcular caudales
import json

duracion=24
hora=8
dow=3
mes=3
curvas=[]
q0=[10.0,15.0,10.0,15.0,10.0,15.0]
qi=[10.0,15.0,10.0,15.0,10.0,15.0]
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

for i in range(duracion):
   fvh = curvas[0][hora]
   fdow = curvas[4][dow]
   fm = curvas[5][mes]
   for j in range(len(q0)):
      qi[j]=round(fvh*fdow*fm*q0[j],2)
   print(f"{qi}")
   #print(f"{i} hora:{hora} dow:{dow} fvh:{fvh} fdow:{fdow} fvm:{fm} q:{qi}")
   hora = (hora + 1) % 24
   if hora==0:
      dow = (dow +1) % 7    
   
   
   