# f_io.py
# Funciones de entrada y salida y otras funciones varias
import math
import sys

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
   #fin de uso()

def cargar_desde_archivo(s_argv):
   #Verificar los parámetros de entrada
   if len(s_argv) < 2 :   #cuando solo se escribe mgh, imprime el modo de uso y termina
     io.uso()
     fin = "input/default.mgh"
     sys.exit()
   else:                     #cuando se da el comando más un nombre de archivo, lo ejecuta en modo normal
     fin = s_argv[1]
     fout = fin + ".out"
     modo = "-n"
   if len(s_argv) == 3 :  #se da comando, archivo, modo
     modo = s_argv[2]
     modo.strip()

   #Abrir el archivo: falta revisar si el archivo existe, si no, debe salir... 
   f = open(fin,'r')

   #Definir las variables globales a usar
   global titulo,autor,fecha,version,viscosidad,imbalance,MaxIt,ns,n,t,factor
   global nn,e,q,nt,de,a,l,d,ks,km,es,op

   #Cargar los datos globales de la corrida
   titulo = f.readline().strip()
   autor = f.readline().strip()
   fecha = f.readline().strip()
   version = f.readline().strip()
   linea = f.readline()
   valores = linea.split(",")
   viscosidad = float(valores[0])
   imbalance = float(valores[1])    
   MaxIt = int(valores[2])
   linea = f.readline()
   valores = linea.split(",")
   ns = int(valores[0])          # nodos de carga fija NS
   n = int(valores[1])           # nodos de demanda NN
   t = int(valores[2])           # numero de tramos NT
   factor = float(valores[3])    # factor de demanda de todos los nudos   
   
   #lee los nudos de carga fija
   #---------------------------
   for i in range(0,ns):
     linea = f.readline()
     valores = linea.split(",")
     nn.append(int(valores[0]))
     e.append(float(valores[1]))
     trash = valores[2].split(" ")
     q.append(float(trash[1]))

   # Leer los nudos de demanda
   # -------------------------
   for i in range(0,n):
     linea = f.readline()
     valores = linea.split(",")
     #trash = valores[2]
     nn.append(int(valores[0]))
     e.append(float(valores[1]))
     q.append(float(valores[2]))

   # Leer los datos de los tramos
   # ----------------------------
   for i in range(0,t):
     linea = f.readline()
     valores = linea.split(",")
     nt.append(int(valores[0]))
     de.append(int(valores[1]))
     a.append(int(valores[2]))
     l.append(float(valores[3]))    
     d.append(float(valores[4]))        
     ks.append(float(valores[5]))    
     km.append(float(valores[6]))    
     es.append(valores[7])    
     op.append(valores[8].strip())
   #Fin de cargar_desde_archivo()  

def imprime_salida_quiet():
   print("quiet: Imprime solo [Q] y [H] finales")

def imprime_salida_normal():
      print("normal: Imprime reporte final")   

def imprime_salida_verbose(final,i):
   if final:
      io.imprime_salida_normal()
   else:
      print("Imprime matrices y vectotres de iteración i")

def revisar_topología(fin):
   # Revisión de la topología de nudo a tramo
   # Se debe asegurar que todos los nodos estén conectados
   global de,a,nn,t,n,ns,titulo,autor,fecha,version
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
   #print("Topología de nudos OK")
