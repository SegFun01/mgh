"""  
 * Calcular números primos
 Calcula 10 número primos nuevos a partir de la lista inicial
 continúa calculando 10 mnumero y los anexa al archivo JSON
"""
import sys
import json
import random

i=0
n=0
ultimo=0
cantidad=0
este=0

with open('./primos.json','r') as primos:
     j_primos = json.load(primos)
     for i in j_primos.keys(): 
        x=j_primos.get(i)  
        print(f"{i}: {x}")
cantidad=len(j_primos)
ultimo=j_primos.get(str(cantidad))
print(f"Ultimo primo({cantidad}) = {ultimo} ")
print("Calculando siguientes 10...")

while n<10:
  esprimo=True
  ultimo=ultimo+2
  p=1
  while p<cantidad:
      este=j_primos.get(str(p))
      if (ultimo % este) == 0:
        esprimo=False
        p=cantidad
      p=p+1  
  if esprimo:    
      cantidad=cantidad+1
      print(f"Primo({cantidad})= {ultimo}")
      j_primos[str(cantidad)]=ultimo
      n=n+1

with open('./primos.json', "w") as outfile:
      json_object = json.dumps(j_primos, indent=4)
      outfile.write(json_object)

#EOF
 
   
   