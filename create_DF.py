import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

Data = pd.read_excel("Datos_SINOLAVE_LRPII.xlsx")
Data.columns = [c.replace(' ', '_') for c in Data.columns]

del Data["CONGESTION_NASAL"]
del Data["DISFONIA"]
del Data["LUMBALGIA"]
del Data["CORIZA"]
del Data["PUERPERIO"]
del Data["DOSIS_VAC_COVID19"]
del Data["DIAS_PUERP"]
del Data["FECHA_TOMA_PRUEBA_RAPIDA"]
del Data["RESULT_PRUEBA_RAPIDA"]
del Data["DESC_RESULT_PRUEBA_RAPIDA"]
del Data["LUGAR_PRUEBA_RAP"]
del Data["FECHA_TOMA_PRUEBA_RAPIDA_2"]
del Data["RESULT_PRUEBA_RAPIDA_2"]
del Data["DESC_RESULT_PRUEBA_RAPIDA_2"]
del Data["LUGAR_PRUEBA_RAP_2"]
del Data["MARCA_VAC_COVID19"]
del Data["FECHA_DOSIS_1"]
del Data["FECHA_DOSIS_2"]
del Data["FOLIO_SINAVE"]
del Data["FOLIO_SINOLAVE"]
del Data["NUMERO_TELEFONICO"]
del Data["MOTIVO_EGRESO"]
del Data["DERECHOHABIENTE"]
del Data["CONSULTORIO"]
del Data["ATAQUE_AL_ESTADO_GENERAL"]
del Data["IRRITABILIDAD_MENOS5AÑOS"]
del Data["OTROS"]
del Data["ESTATUS_CONF1"]
del Data["TIPO_INFLUENZA_CONF1"]
del Data["DESC_OTROS_VIRUS2"]
del Data["RECIBIO_VACUNA"]
del Data["FECHA_EGRESO_UCI"]	
del Data["IND_UCI2"]
del Data["SE_RECONOCE_INDIGENA"]
del Data["ASISTE_PLANTEL_EDUCATIVO"]
del Data["REC_TXANTIVIRD"]
del Data["DESC_OTROS_VIRUS1"]
del Data["EDAD_MESES"]
del Data["EDAD_DIAS"]
del Data["INICIO_SUBITO"]
del Data["ESTATUS_CONF2"]
del Data["CONTACTO_OTROS_CASOS"]
del Data["ANTECED_OTRA"]
del Data["POSTRACION"]
del Data["ESCALOFRIO"]
del Data["SEMANAS_DE_GESTACION"]
del Data["LACTANCIA"]
del Data["ANT_ANEMIA_HEMOLITICA"]
del Data["RECIBIO_VAC_NEUMOCOCO"]
del Data["FIEBRE"]
del Data["TOS"]

Data.dropna(subset = ['FECHA_EGRESO_O_DEFUNCION'], inplace = True)
Data.dropna(subset = ['FECHA_INGRESO'], inplace = True)
Data = Data[Data['EDAD_ANO'] > 3]

#Data["FECHA_INGRESO"].fillna(Data["FECHA_EGRESO_O_DEFUNCION"], inplace = True)
Data['ESTANCIA'] = Data['FECHA_EGRESO_O_DEFUNCION'] - Data['FECHA_INGRESO']
Data['ESTANCIA'] = Data['ESTANCIA'] / np.timedelta64(1,'D')
#Data = Data[Data['ESTANCIA'] > 0  ]

Data['CONDICION_MEDICA'] =  Data['TIENE_INTUBACION_ENDOTRAQUEAL'] 
Data['CONDICION_MEDICA'] += (1.42)*Data['ANTECED_HIPERTENSION'] 
Data['CONDICION_MEDICA'] += (1.58)*Data['ANTECED_DIABETES']
Data['CONDICION_MEDICA'] += (1.40)*Data['ANTECED_CARDIOVASCULAR']
Data['CONDICION_MEDICA'] += (3.19)*Data['ANTECED_CANCER']
Data['CONDICION_MEDICA'] += (1.46)*Data['ANTECED_EPOC']
Data['CONDICION_MEDICA'] += (1.70)*Data['ANTECED_RENAL']
Data['CONDICION_MEDICA'] += (2.81)*Data['ANT_ENF_HEPATICA_CRONICA']
Data['CONDICION_MEDICA'] += (2.29)*Data['DIAG_CLIN_NEUMONIA']
col = "ESTANCIA"


condiciones = [ (Data[col] > 0) & (Data[col] <= 5),
				(Data[col] > 5) & (Data[col] <= 10),
				(Data[col] > 10) & (Data[col] <= 15), 
				(Data[col] > 15) & (Data[col] <= 20),  
				(Data[col] > 20) & (Data[col] <= 25), 
				(Data[col] > 25)]

elecciones = [ 1, 2, 3, 4, 5, 6]
Data["CLASE"] = np.select(condiciones, elecciones, default = 1)

numerics = ['int64', 'float64']
Data = Data.select_dtypes(include=numerics)
Data.to_excel("Condensada_1paso.xlsx")

#corr_matriz = Data.corr(method = "pearson")
#sns.heatmap(corr_matriz,  annot=True)
#plt.xticks(fontsize=5)
#plt.show()
"""
edad_maxima = Data['EDAD_ANO'].max()
print(edad_maxima)
print(Data['EDAD_ANO'] / edad_maxima)
Data.dropna()
Data_filtrados = pd.ExcelWriter("Datos_Filtrados.xlsx")
Data.to_excel(Data_filtrados, index = False)
"""

