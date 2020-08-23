#Leer_datos
import os
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from datetime import datetime,timedelta
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
def leer_datos_xlsx(path,A,B): #A=lineas estudiadas B=casos estudiados
    inicio = datetime(2017,1,1,0)
    fin   = datetime(2017,12,31,23)
    lista_fecha = [(inicio + timedelta(days=d/24)).strftime("%Y-%m-%d %H:%M") for d in range(((fin - inicio).days+1)*24)] 
    lista_fechaM = [(inicio + timedelta(days=d/24)).month for d in range(((fin - inicio).days+1)*24)] 
    lista_fechaH= [(inicio + timedelta(days=d/24)).strftime("%H") for d in range(((fin - inicio).days+1)*24)]  
    lista_fechaD=[(inicio + timedelta(days=d/24)).strftime("%Y-%m-%d") for d in range(((fin - inicio).days+1)*24)]       
    dat=pd.ExcelFile(path+'\Curvas_AC.xlsx')
    C_AC=dat.parse('Hoja1',headers=0,names=['0%','25%','50%','75%','100%']) 
    datos=pd.ExcelFile(path+'\Radiacion.xlsx')
    R=datos.parse('Radiacion',names=['Radiacion']) 
    V_t=[]
    I_t=[]
    P_t=[]
    F_t=[]
    Va_t=[]
    Ia_t=[]
    line_t=[]
    V_s=[]
    I_s=[]
    P_s=[]
    R_s=[]
    Va_s=[]
    Ia_s=[]
    line_s=[]
    caso_s=[]
    date_s=[]
    mes_s=[]
    mes_t=[]
    tipo_s=[]
    tipo_t=[]
    C_ac_s=[]
    C_ac_t=[]
    hora_s=[]
    hora_t=[]
    dia_s=[]
    dia_t=[]
    V_d=[]
    I_d=[]
    P_d=[]
    Va_d=[]
    Ia_d=[]
    for f in range(0,len(B)):     
        datos2=pd.ExcelFile(path+'\\'+B[f]+'.xlsx')
        V=datos2.parse('Hoja1',headers=0,names=A)
        I=datos2.parse('Hoja2',headers=0,names=A) 
        P=datos2.parse('Hoja3',headers=0,names=A)
        Va=datos2.parse('Hoja4',headers=0,names=A)
        Ia=datos2.parse('Hoja5',headers=0,names=A)           
        V_d.append(V)
        I_d.append(I)
        P_d.append(P)
        Va_d.append(Va)
        Ia_d.append(Ia)
        for s in range(0,len(A)):
            V_t=V[A[s]].values.tolist()          
            V_s=V_s+V_t  
            I_t=I[A[s]].values.tolist()          
            I_s=I_s+I_t  
            P_t=P[A[s]].values.tolist()          
            P_s=P_s+P_t  
            Va_t=Va[A[s]].values.tolist()          
            Va_s=Va_s+Va_t  
            Ia_t=Ia[A[s]].values.tolist()          
            Ia_s=Ia_s+Ia_t  
            line_t=[str(A[s]+"("+B[f]+")")]*8760
            line_s=line_s+line_t
            caso_t=[B[f]]*8760
            caso_s=caso_s+caso_t
            R_t=R["Radiacion"].values.tolist()
            R_s=R_s+R_t      
            date_t=lista_fecha
            date_s=date_s+date_t
            mes_t=lista_fechaM
            mes_s=mes_s+mes_t
            hora_t=lista_fechaH
            hora_s=hora_s+hora_t
            C_ac_t=C_AC[B[f]].values.tolist()
            C_ac_s=C_ac_s+C_ac_t 
            dia_t=lista_fechaD
            dia_s=dia_s+dia_t      
    df = pd.DataFrame({"Fecha": date_s,"Dia":dia_s,"Mes":mes_s,"Hora":hora_s,"Tensión": V_s,"Intensidad":I_s,"Vangle":Va_s,"Iangle":Ia_s,"Potencia":P_s,"Radiación":R_s,"Caso":caso_s,"Linea":line_s,"C_ac": C_ac_s})
    return (df,V_d,I_d,P_d,R)