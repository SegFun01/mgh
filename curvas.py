###### LEER LOS DATOS DEL LA RED DESDE UN ARCHIVO DE JSON 
import json

curva1={}
curva2=[]
def leer_json(c_id):
    curva={}
    with open('./projects/PruebaX.pat.json','r') as curvas:
       j_curvas = json.load(curvas)

    print(json.dumps(j_curvas, indent=4))
    print("-----")

    
    for i in (j_curvas['curvas']): # leer los nudos de carga del JSON
       if i.get('id')==c_id:
         curva=i.get('curva')
    return curva
    
x=int(input("Seleccione el id de la curva: "))
curva2=leer_json(x)
print("Curva 2")
print(curva2)
print(f"Un sdolo dato, en [5]: f={curva2[5]}")

