###### LEER LOS DATOS DEL LA RED DESDE UN ARCHIVO DE JSON 

import json


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

leer_json(fin)
print(titulo)
print(autor)
print("Nudos")
print(nn)
print(e)
print(q)
print(fi)
print("Tramos")
print(nt)
print(de)
print(a)
print(l)
print(d)
print(ks)
print(km)
print(es)
print(op)