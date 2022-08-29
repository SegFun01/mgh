import json

file = open("mgh.json","r")
base = json.load(file)
file.close()

print("Titulo:",base["titulo"])
print("Autor:",base["autor"])
print("Fecha:",base["fecha"])
print("Version:",base["version"])
print("Descripcion:",base["descripcion"])
print("Tolerancia del cálculo:",base["tolerancia"])
print("Viscosidad dinámica:",base["viscosidad"])
print("Máximo de iteraciones:",base["max_iteraciones"])
print("Factor de demanda global:",base["factor_demanda_global"])
print("Nudos de carga fija:")
for x in base["nudos_carga"]:
    print("nudo:",x["id"], "| elevacion:",x["elevacion"], "| carga:",x["carga"])
print("Nudos de demanda:")
for y in base["nudos_demanda"]:
    print("nudo:",y["id"], "| elevacion:",y["elevacion"], "| demanda:",y["demanda"], "| factor:",y["factor_demanda"])
for z in base["tramos"]:
    print("Tramo:",z["id"]," :",z["desde"],"->",z["hasta"]," L:",z["longitud"]," D:",z["diametro"]," ks:",z["ks"]," kL:",z["kL"]," Estado:",z["estado"]," Opciones:",z["opciones"])