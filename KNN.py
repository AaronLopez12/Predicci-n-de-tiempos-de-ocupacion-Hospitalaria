import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier

fig = plt.figure(figsize = (10,10))

def Calcular_vector(vector_caracteristicas):
	# Vector caracteristicas con 14 entradas
	resultado = []
	calificacion_vec = (1)*vector_caracteristicas[1]
	calificacion_vec += (1.42)*vector_caracteristicas[2]
	calificacion_vec += (1.58)*vector_caracteristicas[3]
	calificacion_vec += (1.40)*vector_caracteristicas[4] 
	calificacion_vec += (3.19)*vector_caracteristicas[5]
	calificacion_vec += (1.46)*vector_caracteristicas[6] 
	calificacion_vec += (1.70)*vector_caracteristicas[7] 
	calificacion_vec += (2.81)*vector_caracteristicas[8]
	calificacion_vec += (2.29)*vector_caracteristicas[9]
	resultado.append(vector_caracteristicas[0])
	resultado.append(calificacion_vec)
	return resultado

DataFrame 		 = pd.read_excel("Condensada_1paso.xlsx")
tamano    		 = len(DataFrame) 


#### Preprocesamiento de los datos
vecinos = 5
Iteraciones = 50
RES = []
for iteracion in range(Iteraciones):

	random_index = np.random.choice(tamano,
					tamano, replace = False)

	escalador = preprocessing.MinMaxScaler()

	datos = DataFrame[["EDAD_ANO", "CONDICION_MEDICA"]]
	clase = DataFrame["CLASE"]

	datos_muestra = datos.iloc[random_index[0:int((3*tamano)/4)]]
	clase_muestra = clase.iloc[random_index[0:int((3*tamano)/4)]]

	datos_prueba = DataFrame.iloc[
		random_index[int((3*tamano)/4):tamano]]
	
	clase_prueba = clase.iloc[
		random_index[int((3*tamano)/4):tamano]]

	Lista_auxiliar  = []

	for index, row in datos_prueba.iterrows():
		sublist = [row.EDAD_ANO, 
		row.TIENE_INTUBACION_ENDOTRAQUEAL, 
		row.ANTECED_HIPERTENSION, row.ANTECED_DIABETES,
		row.ANTECED_CARDIOVASCULAR, row.ANTECED_CANCER,
		row.ANTECED_EPOC, row.ANTECED_RENAL, 
		row.ANT_ENF_HEPATICA_CRONICA, row.DIAG_CLIN_NEUMONIA]
		Lista_auxiliar.append(sublist)

	Ground_Truth = DataFrame["CLASE"]
	Ground_Truth = Ground_Truth.iloc[
		random_index[int((3*tamano)/4):tamano]]

	Ground_Truth = Ground_Truth.values.tolist()

	#### Creacion del modelo 
	datos_muestra 	= escalador.fit_transform(datos_muestra)
	clasificador 	= KNeighborsClassifier(n_neighbors = vecinos)
	clasificador.fit(datos_muestra, clase_muestra)

	paciente = np.array(Lista_auxiliar)
	Lista_auxiliar2 = []

	for i in range(len(paciente)):
		calificacion_tmp = Calcular_vector(paciente[i])
		Lista_auxiliar2.append(
			[calificacion_tmp[0], calificacion_tmp[1]])

	solicitante = escalador.transform(Lista_auxiliar2)

	Solucion =  clasificador.predict(solicitante)

	accuracy = 0

	for jj in range(len(Ground_Truth)):
		if Ground_Truth[jj] == Solucion[jj]:
			accuracy += 1

	RES.append(100* accuracy/len(Ground_Truth))

print("---------------------------------------------------")
print("Resultados del experimento")
print("Promedio de las precisiones: ",np.mean(RES))
print("Desviacion estandar de las precisiones: ", np.std(RES))
print("Intervalo de Confianza: [",
	np.mean(RES) - (1.96)*(np.std(RES)/ np.sqrt(len(Ground_Truth))),
	",", 
	np.mean(RES) + (1.96)*(np.std(RES)/ np.sqrt(len(Ground_Truth))),
	 "]")
print("---------------------------------------------------")