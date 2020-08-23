#1_CurvaDiaria
import os
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from datetime import datetime,timedelta
from plotly.subplots import make_subplots
import plotly.express as px

def Plot_Curva_Diaria(V_d,I_d,P_d,R,A,B,path):  
    C=["Tensión","Intensidad","Potencia","Radiación"]
    inicio = datetime(2017,1,1,0)
    fin   = datetime(2017,12,31,23)
    lista_fecha2 = [(inicio + timedelta(days=h/24)).strftime("%H:%M") for h in range(0,24)] 
    #Se definen las etiquetas de cada plot
    legend_g=[]
    for n in range(0,len(B)):
        for i in range(0,len(A)):
            legend_g.append(str(A[i]+"("+ B[n]+ ")"))

    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,                        
                        vertical_spacing=0.1,
                        subplot_titles=C)
    #Se añaden los perfiles de tensión, intensidad, potencia y radiación uno en cada fila del subplot
    for s in range(0,len(B)):
        for n in range(0,len(A)):        
                fig.add_trace(
                    go.Scattergl(
                        mode='lines',                        
                        showlegend=True,
                        legendgroup=legend_g[len(A)*s+n],
                        line=dict(color=px.colors.qualitative.Prism[((s+len(B)*n)*2)%11],width=3),
                        name=legend_g[len(A)*s+n],
                        x=lista_fecha2,
                        y=[(V_d[s][A[n]][h]) for h in range(0,24)]            
                    ),
                    row=1, 
                    col=1
                )
                fig.add_trace(
                    go.Scattergl(
                        mode='lines',                        
                        showlegend=False,
                        legendgroup=legend_g[len(A)*s+n],
                        line=dict(color=px.colors.qualitative.Prism[((s+len(B)*n)*2)%11],width=3),
                        name=legend_g[len(A)*s+n],
                        x=lista_fecha2,
                        y=[(I_d[s][A[n]][h]) for h in range(0,24)]               
                    ),
                    row=2, 
                    col=1
                )
                fig.add_trace(
                    go.Scattergl(
                        mode='lines',                        
                        showlegend=False,
                        legendgroup=legend_g[len(A)*s+n],
                        line=dict(color=px.colors.qualitative.Prism[((s+len(B)*n)*2)%11],width=3),
                        name=legend_g[len(A)*s+n],
                        x=lista_fecha2,
                        y=[(P_d[s][A[n]][h]) for h in range(0,24)]                
                    ),
                    row=3, 
                    col=1
                ) 
    fig.add_trace(
        go.Scatter(
            mode='lines',
            visible=True,
            showlegend=True,
            line=dict(width=3),
            name="Irradiancia",
            x=lista_fecha2,
            y=[R["Radiacion"][h] for h in range(0,24)]  
        ),
        row=4, 
        col=1
    ) 
    #Se definen las propiedades de los ejes
    fig.update_xaxes(nticks=24,row=4, col=1)
    fig.update_yaxes(title_text="Tensión (V)",nticks=5,row=1, col=1)
    fig.update_yaxes(title_text="Intensidad (A)",nticks=5, row=2, col=1)
    fig.update_yaxes(title_text="Potencia (kW)",nticks=5, row=3, col=1)
    fig.update_yaxes(range=[0,1400],nticks=5,title_text="Irradiancia (W/m²)", row=4, col=1) 

    #Se añaden los botones para variar el caso de estudio
    F_t=[]
    for f in range(0,len(B)): 
        F=[False] * len(fig.data)
        F[(3*len(A)*f):(3*len(A)*(f+1))]=[True]*3*len(A)
        F[len(fig.data)-1]=True
        F_t.append(F)
    F=[True]*len(fig.data)
    F_t.append(F)
    F=[True]*3*len(A)+[False]*3*len(A)+[True]*3*len(A)+[False]*3*len(A)+[True]*3*len(A)+[True]
    F_t.append(F)

    botones=[]
    for i in range(0,len(B)):
        d=dict(label=B[i],
            method="update",
            args=[{"visible": F_t[i]},
            ])
        botones.append(d)
    d=dict(label="All",
        method="update",
        args=[{"visible": F_t[len(B)]},
        ])
    botones.append(d)
    d=dict(label="0%-50%-100%",
        method="update",
        args=[{"visible": F_t[len(B)+1]},
        ])
    botones.append(d)
    #Se añaden los botones al layout
    fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            type = "buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.025,
            xanchor="left",
            y=1.2,
            yanchor="top",
            buttons= botones                              
        )])
     #Se crean los escalones del Slider y se añaden
    steps = []

    for i in range(0,365):
        b=[]
        for s in range(0,len(B)):
            for n in range(0,len(A)):        
                V_v=[(V_d[s][A[n]][h]) for h in range(i*24,i*24+24)]
                b.append(V_v)
                I_v=[(I_d[s][A[n]][h]) for h in range(i*24,i*24+24)]
                b.append(I_v)
                P_v=[(P_d[s][A[n]][h]) for h in range(i*24,i*24+24)]
                b.append(P_v)
        R_v=[R["Radiacion"][h] for h in range(i*24,i*24+24)]
        b.append(R_v)  
        step = dict(
                method="restyle",
                args=["y",b], 
                label=(inicio + timedelta(days=i)).strftime("%d-%m")
            )
        steps.append(step) 
    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Fecha: "},
        pad={"t": 30},
        steps=steps
    )]
    fig.update_layout(
        sliders=sliders,
        width=1350,
        height=650,
        font=dict(size=10),
          
    )
    pio.write_html(fig, file=path+'\Curva_diaria_1.html', auto_open=True)
