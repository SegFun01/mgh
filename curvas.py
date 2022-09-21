###### LEER LOS DATOS DEL LA RED DESDE UN ARCHIVO DE JSON 
import json

curvas=[]

def get_curva():
    m_curva=[]
    with open('./input/curvas.json','r') as curvas:
       j_curvas = json.load(curvas)
    d_curvas=j_curvas.get('curvas')
    for i in d_curvas:   
      m_curva.append(d_curvas.get(c_id))
    return m_curva
    
curvas=get_curva()
print("Curvas")
print(curvas)

