###### LEER LOS DATOS DEL LA RED DESDE UN ARCHIVO DE JSON 
import json

curvas=[]

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
print("Curvas")
print(curvas)
for i in len(curvas):
   print(f"{i} {curvas[i]}")
