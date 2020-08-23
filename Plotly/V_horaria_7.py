# mymod4.py
import os
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from datetime import datetime,timedelta
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
def Plot_V_horaria(df,A,B,path):
    #Leo datos 
    os.makedirs(path+'\V_horaria_7', exist_ok=True)   
    meses=[]
    legend_g=[]
    for x in range(0,12):
        meses.append(datetime(2017,(x+1),1,0).month)
    print(meses)   

    for i in range(0,len(A)):
        for n in range(0,len(B)):
            legend_g.append(str(A[i]+"("+B[n]+")"))
   
    fig = make_subplots(rows=3, cols=4,
                        shared_yaxes=True,
                        vertical_spacing=0.1,
                        horizontal_spacing=0.01,
                        subplot_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        x_title="Horas del día"
                    )     
    min_1=[]     
    max_1=[]  
    for n in range(0,len(A)):  
        for s in range(0,len(B)):
            for m in range(0,12): 
            
                if m==0:
                    F=True
                else:
                    F=False
                fig.add_trace(
                    go.Scattergl(
                        mode='markers',
                        visible=True,
                        showlegend=F,
                        legendgroup=legend_g[s+len(B)*n],
                        marker=dict(color=px.colors.qualitative.Prism[((s+len(B)*n)*2)%11],size=2,opacity=0.6),
                        name=legend_g[s+len(B)*n],
                        x=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Hora"],
                        y=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"],                                   
                    ),
                    row=(m//4)+1,
                    col=(m%4)+1

                    )
                f=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"])
                ff=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"]) 
                min_1.append(f)              
                max_1.append(ff)         
            
    fig.update_xaxes(range=[0,24],nticks=24)  
    fig.update_yaxes(range=[min(min_1)-abs(0.01*min(min_1)),max(max_1)+abs(0.01*min(min_1))]) 
    fig.update_yaxes(title_text="Tensión (V)",col=1,row=1)  
    fig.update_yaxes(title_text="Intensidad (A)",col=1,row=2)  
    fig.update_yaxes(title_text="Potencia (W)",col=1,row=3) 
    F_t=[]
    for f in range(0,len(A)):
        F=[False] * len(fig.data)
        F[(len(B)*12*f):(len(B)*12*(f+1))]=[True]*len(B)*12
        F_t.append(F)     
    F=[True]* len(fig.data)
    F_t.append(F) 
    #Update menu
    botones=[]
    for  t in range(0,len(A)):
        d=dict(label=A[t],
                method="update",
                args=[{"visible": F_t[t]},
            ])    
        botones.append(d) 
    d=dict(label="All",
                method="update",
                args=[{"visible": F_t[len(A)]},
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
        font=dict(size=10) 
    )
    pio.write_html(fig, file=path+'\V_horaria_7'+'.html', auto_open=True)


    for n in range(0,len(A)): 
        fig = make_subplots(rows=3, cols=4,
                        shared_yaxes=True,
                        vertical_spacing=0.1,
                        horizontal_spacing=0.02,
                        subplot_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        x_title="Horas del día"
                    )     
        min_1=[]     
        max_1=[]  
        for s in range(0,len(B)):
            for m in range(0,12):          
                if m==0:
                    F=True
                else:
                    F=False
                fig.add_trace(
                    go.Scattergl(
                        mode='markers',
                        visible=True,
                        showlegend=F,
                        legendgroup=legend_g[s+len(B)*n],
                        marker=dict(color=px.colors.qualitative.Prism[((s+len(B)*n)*2)%11],size=2,opacity=0.6),
                        name=legend_g[s+len(B)*n],
                        x=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Hora"],
                        y=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"],                                   
                    ),
                    row=(m//4)+1,
                    col=(m%4)+1
                    )
                f=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"])
                ff=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"]) 
                min_1.append(f)              
                max_1.append(ff)          
                    
        print(len(fig.data))
        fig.update_xaxes(range=[0,24],nticks=24)  
        fig.update_yaxes(range=[min(min_1)-abs(0.01*min(min_1)),max(max_1)+abs(0.01*max(max_1))]) 
        fig.update_yaxes(title_text="Tensión (V)",col=1,row=1)  
        fig.update_yaxes(title_text="Intensidad (A)",col=1,row=2)  
        fig.update_yaxes(title_text="Potencia (W)",col=1,row=3)   
        fig.update_layout(       
            width=1350,
            height=650,
            font=dict(size=10) 
        )
        pio.write_html(fig, file=path+'\V_horaria_7\V_h_'+A[n]+'.html', auto_open=False)