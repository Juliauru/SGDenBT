import os
import numpy as np
import pandas as pd
import Leer_datos
import CurvaDiaria_1
import VIP_anual_TY_2
import V230_DP_3
import R_Autoconsumo_4
import Relacion_0_5
import V0_DP_6
import V_horaria_7
import DP_VIP_h_8
import Iangle_9
#Estocolmo
#A=['line6','line20','line56','line151','line234','line238','line240','line244','line194','line73','line76']
#Benimamet
#A=['line1','line2','line4','line41','line69','line116','line221','line239','line266',
 #  'line139','line211','line226','line230','line233','line188','line155']
#Godella
A=['line53','line46','line43','line44','line45','line48','line28','line75','line71','line17']
B=['0%','25%','50%','75%','100%']
path=os.getcwd()+'\Resultados'
(df,V_d,I_d,P_d,R)=Leer_datos.leer_datos_xlsx(path,A,B)
print(len(df))
CurvaDiaria_1.Plot_Curva_Diaria(V_d,I_d,P_d,R,A,B,path)
VIP_anual_TY_2.Plot_VIP_Irradiancia(df,A,B,path)

R_Autoconsumo_4.Plot_R_CG(df,A,B,path)
Relacion_0_5.Plot_R_0(df,A,B,path)
V0_DP_6.Plot_VR0(df,A,B,path)

DP_VIP_h_8.Plot_V_h(df,A,B,path)
Iangle_9.Plot_Iangle(df,A,B,path)

#V_horaria_7.Plot_V_horaria(df,A,B,path)
#V230_DP_3.Plot_V230_DP(df,A,B,path)