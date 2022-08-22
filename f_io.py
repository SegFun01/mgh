# f_var.py
# Otras funciones varias
import math
# Hacer las funciones de impresión de salida aquí
# Hacer la función de revisión topológica aquí

def uso():
   print("")
   print("Modo de uso:  python mgh.py nombre_archivo.mgh opcion")
   print("-----------------------------------------------------")
   print( "")
   print("Opciones:")
   print("-n: modo normal, por defecto, imprime tablas de datos de entrada y salida")
   print("")
   print("-q: modo silencioso, solo imprime los vectores H y Q, de alturas piezométricas")
   print("    en los nudos y caudales en los tramos")
   print("")
   print("-v: modo elocuente, imprime tablas de datos de entrada y salida, todos los vec-")
   print("    tores y matrices; y los resultados de cada iteración")
   print("")
   print("Observaciones:")
   print("La salida del programa va dirigida a la consola: \"stdout\".")
   print("Para redirigir la salida use entubamiento con > o con >>")
   print("")
   print("Ejemplo: python mgh.py ./input/default.mgh -v > ./output/default.mgh.out")
   print("")