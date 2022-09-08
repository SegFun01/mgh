###### LEER LOS DATOS DEL LA RED DESDE UN ARCHIVO DE JSON 

import json
import sys

nn = []
nt = []
e = []
q = []
fi = []
h = []
de = []
a = []
l = []
d = []
ks = []
km = []
es = []
op = []

fin = "./input/default.mgh.json"
fout = fin + ".out"
titulo="Titulo de la red"
autor="Carlos Camacho Soto"
fecha="21/03/1966"
version="1.0.0"
viscosidad=1.007E-6
imbalance=1.0E-5
MaxIt=40
ns=1
n=5
t=7
factor=1
modo="-n"
ecuacion="S"        # Ecuación por defecto a usar Swamee-Jain, alternativa C=Colebrook-White
tol= 1E-6
duracion = 0
descripcion = ""

#---------->>>>>>>>>> verificar nombre archivo entrada
def input_check(fin):
   if "/" not in fin:
      fin= "./input/" + fin # si no se especifica directorio se usa ./input por defecto
   if ".mgh" not in fin:
      fin = fin + ".mgh"    # si no se especifica extension se usa mgh por defecto
   if ".json" not in fin:
      fin = fin + ".json"    # si no se especifica extension se usa json por defecto
   return fin

#--------->>>>>>>>>>> verificar nombre archivo de salida
def output_check(fout):
   lista = fout.split("/")
   x = len(lista)
   fout = lista[x-1]
   fout = "./output/" + fout  # se cambia el directorio por ./output/    
   fout = fout + ".out"       # se especifica extensión .mgh.out
   return fout    

def crea_red():
   global fin
   d_red = {}
   miLista = []
   miDict  = {}
   print("------> METODO DEL GRADIENTE HIDRÁULICO <-------")
   print("     Construcción de red en modo interactivo")
   print("-------------------------------------------------")
   fin = input("Escriba el nombre del archivo de entrada a crear: ")
   fin = input_check(fin)
   print("-----")
   miVar = input("Título de la red a modelar: ")
   d_red["titulo"]=miVar
   miVar  = input("Autor del modelo          : ")
   d_red["autor"]=miVar
   miVar  = input("Fecha                     : ")
   d_red["fecha"]=miVar
   version = input("Versión de corrida        : ")
   d_red["version"]= miVar
   miVar = input("Viscosidad cinemática     : ")
   d_red["viscosidad"]=float(miVar)
   miVar = input("Desbalance de Q aceptado  : ")
   d_red["imbalance"]=float(miVar)
   miVar = input("Iteraciones permitidas    : ")
   d_red["max_iteraciones"]=int(miVar)
   miVar= input("Ecuación para f: C ó S    : ")
   d_red["ecuacion"]= miVar
   miVar= input("Tolerancia en cálculo de f:")
   d_red["tolerancia"]= miVar
   miVar = input("Factor global de demanda  : ")
   d_red["factor_demanda_global"]= float(miVar)
   print("----------------")
   ns = int(input("Cantidad de nodos de carga fija : "))
   print ("Nudo  Elev Carga ")
   nc=[] 
   for i in range(ns):
      cadena = input(f"{i}   :  ")
      lista = cadena.split()
      nc.append({ "id": i, "elevacion": float(lista[0]), "carga":float(lista[1])})
      # print(nc)
   d_red["nudos_carga"]= nc
   # print(d_red)
   nd = []
   # x = input("Pausa, pulse <enter>")
   print("----------------")
   n = int(input("Cantidad de nodos de demanda : "))
   print ("Nudo Elev Demanda Factor ") 
   for i in range(n):
      cadena = input(f"{i+ns} : ")
      lista = cadena.split()
      nd.append({ "id": i+ns, "elevacion": float(lista[0]), "demanda": float(lista[1]), "factor": float(lista[2]) }) 
      # print(nd)
   d_red["nudos_demanda"]= nd 
   # print(d_red)
   # x = input("Pausa, pulse <enter>")
   t = int(input("Cantidad de tramos : "))
   print ("Tramo de  a  L  D   Ks  KL Es Op") 
   tr =[]
   for i in range(t):
      cadena = input(f"{i}  :  ")
      lista = cadena.split()
      tr.append({ "id": i, "desde": int(lista[0]), "hasta": int(lista[1]), "longitud": float(lista[2]), "diametro": float(lista[3]), "ks":float(lista[4]), "kL": float(lista[5]), "estado": lista[6], "opciones": lista[7] })  
   d_red["tramos"]= tr
   d_red["signature"]="#EOF- crcs-2022"
   #print(d_red)
   print("")
   # Serializing json
   json_red = json.dumps(d_red, indent=4)
   # x = input("Pausa, pulse <enter>")
   # print(json_red)
   # Writing to sample.json
   with open(fin, "w") as outfile:
      outfile.write(json_red)

def mostrar_json(fin):
   with open(fin,'r') as red:
      j_red = json.load(red)
   print(json.dumps(j_red, indent=4))


def leer_json(fin):
    global nn,nt,e,q,fi,h,de,a,l,d,ks,km,es,op
    global titulo, autor, fecha, version, viscosidad, descripcion
    global imbalance, MaxIt, factor, ecuacion, tol, duracion
    global ns, n, t 
    with open(fin,'r') as red:
       j_red = json.load(red)

    print(json.dumps(j_red, indent=4))
    print("-----")
    
    ns = len(j_red['nudos_carga'])
    n  = len(j_red['nudos_demanda'])
    t  = len(j_red['tramos'])
    titulo = j_red.get('titulo')
    autor = j_red.get('autor')
    fecha = j_red.get('fecha')
    version = j_red.get('version')
    viscosidad = j_red.get('viscosidad')
    imbalance = j_red.get('imbalance')
    MaxIt = j_red.get('max_iteraciones')
    tol = j_red.get('tolerancia')
    factor = j_red.get('factor_demanda_global')
    ecuacion = j_red.get('ecuacion')
    duracion = j_red.get('duracion')
    descripcion = j_red.get('descripcion')
    
    for i in (j_red['nudos_carga']): # leer los nudos de carga del JSON
       nn.append(i.get('id'))
       e.append(i.get('elevacion'))
       q.append(i.get('carga'))
       h.append(i.get('carga'))  

    for i in (j_red['nudos_demanda']): # leer los nudos de demanda del JSON
       nn.append(i.get('id'))
       e.append(i.get('elevacion'))
       q.append(i.get('demanda'))
       fi.append(i.get('factor'))

    for i in (j_red['tramos']):  # leer los tramos del JSON
       nt.append(i.get('id'))
       de.append(i.get('desde'))
       a.append(i.get('hasta'))
       l.append(i.get('longitud'))
       d.append(i.get('diametro'))
       ks.append(i.get('ks'))
       km.append(i.get('kL'))
       es.append(i.get('estado'))
       op.append(i.get('opciones'))

crea_red()
parada = input("Archivo JSON creado! pulse <enter> para verlo en terminal ")
mostrar_json(fin)

# leer_json(fin)
