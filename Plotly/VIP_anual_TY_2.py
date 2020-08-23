# VIP_anual_TY
import os
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from datetime import datetime,timedelta
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px

def Plot_VIP_Irradiancia(df,A,B,path):
    meses=[]
    legend_g=[]
    for x in range(0,12):
        meses.append(datetime(2017,(x+1),1,0).month)
    print(meses)   
    for i in range(0,len(A)):
        for n in range(0,len(B)):
            legend_g.append(str(A[i]+"("+B[n]+")"))
    
  
    fig = make_subplots(rows=3, cols=12,
                        shared_yaxes=True,
                        vertical_spacing=0.04,
                        horizontal_spacing=0.01,
                        column_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        x_title="Irradiancia (W/m²)"
                    )  
    C=["Tensión","Intensidad","Potencia"]                           
    for n in range(0,len(A)):  
        for s in range(0,len(B)):
            for m in range(0,12): 
                for l in range(3):
                    if m==0 and l==0:
                        LV=True
                    else:
                        LV=False

                    fig.add_trace(
                        go.Scattergl(
                            mode='markers',                      
                            showlegend=LV,
                            legendgroup=legend_g[s+len(B)*n],
                            marker=dict(color=px.colors.qualitative.Prism[((s+len(B)*n)*2)%11],size=2),
                            name=legend_g[s+len(B)*n],
                            x=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Radiación"],
                            y=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))[C[l]]               
                        ),
                        row=l+1, 
                        col=m+1
                    )           
    #Se actualizan los ejes para adaptarse a las necesidades              
    print(len(fig.data))
    fig.update_yaxes(title_text="Tensión (V)", row=1, col=1)
    fig.update_yaxes(title_text="Intensidad (A)", row=2, col=1)
    fig.update_yaxes(title_text="Potencia (kW)", row=3, col=1)
    fig.update_xaxes(range=[0,1400])
    #Update menu
    print(len(A))
    print(len(fig.data))
    print(len(B))
    F_t=[]
    for f in range(0,len(A)):
        F=[False]*len(fig.data)
        F[(len(B)*12*3*f):(len(B)*12*3*(f+1))]=[True]*(len(B)*12*3) 
        F_t.append(F)   
    botones=[]
    for t in range(0,len(A)):
        d=dict(label=A[t],
                method="update",
                args=[{"visible": F_t[t]},
            ])
        botones.append(d) 
    d=dict(label="All",
            method="update",
            args=[{"visible": [True]*len(fig.data)}
        ])
    botones.append(d) 

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
                buttons=botones
            
            )
        ])
    fig.update_layout(        
        width=1350,
        height=650,
        font=dict(size=10),
        legend= {'itemsizing': 'constant'}
               
        )
    pio.write_html(fig, file=path+'\VIP_anual_TY_2'+'.html', auto_open=True)

