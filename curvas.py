###### LEER LOS DATOS DEL LA RED DESDE UN ARCHIVO DE JSON 
import json

curva1=[]

def get_curva(c_id):
    curva=[]
    with open('curvas.json','r') as curvas:
       j_curvas = json.load(curvas)
    curva=i.get(c_id)
    return curva
    
x=input("Seleccione el id de la curva: ")
curva1=get_curva(x)
print("Curva 1")
print(curva1)
print(f"Un sdolo dato, en [5]: f={curva1[5]}")

