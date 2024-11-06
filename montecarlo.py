"""  
 * Aleatoriamente selecciona valores de caudal demandado de acuerdo con el nivel de probabilidad
   Hace un vector con 100 (o más valores) y luego hace una corrida de Montecarlo
   Para obtener un valor probabilístico del caudal
  Es parte de la modelación, para deninir caudales en los nudos

"""
import numpy
import json
import random
n = 1000
f_n= float(n)
c_prob = [(20, 5.0),(65, 7.5),(15,9.5)]
q = []
qmc=0.0
QT=0.0
random.seed()

# Se crean 100 valores a partir de los 3 caudales posibles en cantidades de acuerdo a su probabilidad
# en este ejemplo hay 20 valores de 5 l/s, 65 de 7.5 l/s y 15 de 9.5
for i in range(len(c_prob)):      # esto se realiza las veces requeridas en el periodo extendido
   for j in range(c_prob[i][0]):
      q.append(c_prob[i][1])

# Se obtienen n valores aleatorios entre 0 y 99 para obtener el valor del dato probabilistico para ese tirado de dado
for i in range(n):
      j=random.randint(0,99)
      print(f"q{i}={q[j]}")
      QT=QT+q[j]

# Se promedia entre los n tirados de dado
qmc = QT/f_n

print(f"q={qmc}")
      
   
   