"""  
 * Aleatoriamente selecciona valores de caudal demandado de acuerdo con el nivel de probabilidad
   Hace un vector con 100 (o más valores) y luego hace una corrida de Montecarlo
   Para obtener un valor probabilístico del caudal
  Es parte de la modelación, para deninir caudales en los nudos

"""
import numpy
import json
import random
n = 100
c_prob = [(20, 5.0),(65, 7.5),(15,9.5)]
q = []
qmc=0.0
QT=0.0
random.seed()

for i in range(3):      # esto se realiza las veces requeridas en el periodo extendido
   for j in range(c_prob[i][0]):
      q.append(c_prob[i][1])

for i in range(100):
      j=random.randint(0,99)
      print(f"q{i}={q[j]}")
      QT=QT+q[j]

qmc = QT/100.0

print(f"q={qmc}")

      
   
   