# f_io.py
# Funciones de entrada y salida y otras funciones varias
#import math
import sys
import numpy as np


# Hacer las funciones de impresión de salida aquí
# Hacer la función de revisión topológica aquí

#---------->>>>>>>>> Función que imprime el modo de uso
def uso():
   print("")
   print("                    METODO DEL GRADIENTE HIDRÁULICO              crcs 2022")
   print("--------------------------------------------------------------------------")
   print("")
   print("Modo de uso:  python mgh.py nombre_archivo.mgh opcion")
   print("")
   print("Opciones:")
   print("")
   print("-n: modo normal, por defecto, imprime tablas de datos de entrada y salida")
   print("")
   print("-q: modo silencioso, solo imprime los vectores H y Q finales")
   print("")
   print("-v: modo detallado, imprime tablas de datos de entrada y salida, los vec-")
   print("    tores y matrices y los resultados de cada iteración")
   print("")
   print("Observaciones:")
   print("La salida del programa va dirigida a la consola: \"stdout\".")
   print("Para redirigir la salida use entubamiento con > o con >>")
   print("")
   print("Ejemplo: python3 mgh.py ./input/default.mgh -v > ./output/default.mgh.out")
   print("-------------------------------------------------------------------------")
#----------Fin de uso()

#---------->>>>>>>>>> Función para imprimir los datos de salida en modo quiet
def imprime_salida_quiet():
   print("quiet: Imprime solo [Q] y [H] finales")
#-----------

#---------->>>>>>>>>> Función que imprime la salida normal: tablas de nudos y tramos
def imprime_salida_normal():
      print("normal: Imprime reporte final")   
#----------      

#---------->>>>>>>>>> Función que imprime las matrices de cada iteración
def imprime_salida_verbose(final,i):
   if final:
      io.imprime_salida_normal()
   else:
      print("Imprime matrices y vectotres de iteración i")
#----------

#---------->>>>>>>>>> Función que revisa la topología de la red, termina si hay error y lo indica
def revisar_topologia(t,fin,n,ns,nn,de,a,titulo,autor,fecha,version,modo):
   notOK=[]
   errores=0
   for i in range(n+ns):
      nudosOK=False
      for j in range(t):
         if de[j]==nn[i] or a[j]==nn[i]:
            nudosOK=True
      if nudosOK==False:
         notOK.append(nn[i])
         errores= errores+1       
   if errores>0:
      print("--")
      print("MÉTODO DEL GRADIENTE HIDRÁULICO")
      print("--")
      print("Archivo de entrada:", fin)
      print("Titulo:     ",titulo)
      print("Autor:      ",autor)
      print("Fecha:      ",fecha)
      print("Versión:    ",version)
      print("--")
      print("Error en la topología de nudos y tramos: nudos sin conexión")
      print("Revise los siguientes nudos: ",notOK)
      print("--")
      sys.exit()
   if modo =="-v":   
     print("Topología de nudos OK")
     print("")
#----------

#---------->>>>>>>>>> Imprimir matrices de una lista
def imprime_matrices(matrices,nombres):
   # a partir de una lista de matrices y una lista de sus nombres imprime cada matriz de la lista
   j=0
   for i in matrices:
      print(f"Matriz [{nombres[j]}]")
      print(f"{i}")
      print("")
      j=j+1
   
#---------->>>>>>>>>> Imprimir lista de variables hidráulicas de los nudos
def imprime_hid(nt, de, a, l, d, ks, km, es, op, At, v, Re, f, hf, hm, alfa,t):
   print("Variables hidráulicas de los tramos")   
   print("")
   print("  N  De->A    L    D    ks    kL   Es    A     v      Re     f       hf    hL    alfa")
   print("---------------------------------------------------------------------------------------")
   for i in range(t):
       print(f"{nt[i]:>3} {de[i]:>3}{a[i]:>3} {l[i]:5.0f} {d[i]:4.0f} {ks[i]:5.4f} {km[i]:4.1f} {es[i]:>3} {At[i]:7.4f} {v[i]:4.2f} {Re[i]:7.0f} {f[i]:6.5f} {hf[i]:5.2f} {hm[i]:5.2f} {alfa[i]:8.2f}" )
   print("---------------------------------------------------------------------------------------")

#---------->>>>>>>>>> Imprimir matrices para verificación
def matrices_check(Ho,qi,H,Q,B,BT,C,I,N,At,v,Re,f,hf,hm,alfa,A,A1):
  print("Matriz cargas fijas:",Ho) 
  print("Matriz demandas:",qi) 
  print("Matriz de cargas en nudos:",H)
  print("Matriz de caudales en los tramos: Q")
  print(Q)
  print("Topología nudos de carga fija: C")
  print(C)
  print("Topología de tramos-nudos: B")
  print(B)
  print("Transpuesta de B: BT")
  print(BT)
  print("Matriz identidad: I")
  print(I)
  print("Matriz de potencias de la ecuación de pérdidas: N")
  print(N)
  print("Areas de los tramos: At") 
  print(At)
  print("Velocidades en los tramos: v")
  print(v)
  print("Número de Reynolds de los tramos: Re")
  print(Re)
  print("Coeficientes de pérdidas de los tramos: f")
  print(f)
  print("Pérdidas por fricción en los tramos: hf")
  print(hf)
  print("Pérdidas locales en los tramos: hm")
  print(hm)
  print("Coeficientes alfa de los tramos: alfa")
  print(alfa)
  print("Matriz de valores alfa: A")
  print(A)
  print("Matriz de valores alfa: A'")
  print(A1)
#----------