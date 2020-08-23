# mymod4.py
import os
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from datetime import datetime,timedelta
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
def Plot_R_0(df,A,B,path):

    os.makedirs(path+'\R0_5', exist_ok=True)
    meses=[]
    legend_g=[]
    for x in range(0,12):
        meses.append(datetime(2017,(x+1),1,0).month)
    print(meses)   

    for i in range(0,len(A)):
        for n in range(1,len(B)):
            legend_g.append(str(A[i]+"("+B[n]+")"))
 

    fig = make_subplots(rows=3, cols=12,
                            shared_yaxes=True,
                            vertical_spacing=0.05,
                            horizontal_spacing=0.01,
                            column_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                            x_title="Valores (Tensión(V), Intensidad(A), Potencia(kW)) con penetración 0%"
                        ) 
    min_1=[[],[],[]]
    max_1=[[],[],[]]      
    C=["Tensión","Intensidad","Potencia"]      
    for n in range(0,len(A)):  
        for s in range(0,(len(B)-1)):
            for m in range(0,12): 
                for l in range(3):
                    if m==0 and l==0:
                        FV=True
                    else:
                        FV=False
                    fig.add_trace(
                        go.Scattergl(
                            mode='markers',
                            visible=True,
                            showlegend=FV,
                            legendgroup=legend_g[s+(len(B)-1)*n],
                            marker=dict(color=px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11],size=2),
                            name=legend_g[s+(len(B)-1)*n],
                            x=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))[C[l]],
                            y=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))[C[l]]               
                        ),
                        row=l+1, 
                        col=m+1
                    ) 
                    f=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))[C[l]])
                    ff=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))[C[l]]) 
                    min_1[l].append(min(f,ff))   
                    f=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))[C[l]])
                    ff=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))[C[l]]) 
                    max_1[l].append(max(f,ff))       
                    
    print(len(fig.data))
    r_1=[min(min_1[0])-min(min_1[0])*0.01,max(max_1[0])+max(max_1[0])*0.01]
    r_2=[min(min_1[1])-min(min_1[1])*0.05,max(max_1[1])+max((max_1[1]))*0.05]
    r_3=[min(min_1[2])-min(min_1[2])*0.05,max(max_1[2])+max((max_1[2]))*0.05]
    for i in range(12):
                fig.update_xaxes(range=r_1, row=1,col=i+1)
                fig.update_xaxes(range=r_2, row=2,col=i+1)
                fig.update_xaxes(range=r_3, row=3,col=i+1)
                fig.update_yaxes(range=r_1, row=1,col=i+1)
                fig.update_yaxes(range=r_2, row=2,col=i+1)
                fig.update_yaxes(range=r_3, row=3,col=i+1)
            

    fig.update_yaxes(title_text="Tensión (V)", row=1, col=1)
    fig.update_yaxes(title_text="Intensidad (A)", row=2, col=1)
    fig.update_yaxes(title_text="Potencia (kW)", row=3, col=1)

    #Update menu
    F_t=[]
    for f in range(0,len(A)):
        F=[False] * len(fig.data)
        F[((len(B)-1)*3*12*f):((len(B)-1)*3*12*(f+1))]=[True]*(len(B)-1)*3*12
        F_t.append(F)     
    F=[True]* len(fig.data)
    F_t.append(F) 

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
        font=dict(size=10),
        legend= {'itemsizing': 'constant'},
    )
    pio.write_html(fig, file=path+'\VIP_anual_R_0_5'+'.html', auto_open=True)
    for n in range(0,len(A)):  
        fig = make_subplots(rows=3, cols=12,
                            shared_yaxes=True,
                            vertical_spacing=0.05,
                            horizontal_spacing=0.01,
                            column_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                            x_title="Valores (Tensión(V), Intensidad(A), Potencia(kW)) con penetración 0%"
                        ) 
        min_1=[[],[],[]]
        max_1=[[],[],[]]
        max_2=[]
        max_3=[]
        for s in range(0,(len(B)-1)):
            for m in range(0,12): 
                for l in range(3):
                    if m==0 and l==0:
                        FV=True
                    else:
                        FV=False
                    fig.add_trace(
                        go.Scattergl(
                            mode='markers',
                            visible=True,
                            showlegend=FV,
                            legendgroup=legend_g[s+(len(B)-1)*n],
                            marker=dict(color=px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11],size=2),
                            name=legend_g[s+(len(B)-1)*n],
                            x=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))[C[l]],
                            y=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))[C[l]]               
                        ),
                        row=l+1, 
                        col=m+1
                    ) 
                    f=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))[C[l]])
                    ff=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))[C[l]]) 
                    min_1[l].append(min(f,ff))   
                    f=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))[C[l]])
                    ff=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))[C[l]]) 
                    max_1[l].append(max(f,ff))       
                    
        print(len(fig.data))
        r_1=[min(min_1[0])-min(min_1[0])*0.01,max(max_1[0])+max(max_1[0])*0.01]
        r_2=[min(min_1[1])-min(min_1[1])*0.05,max(max_1[1])+max((max_1[1]))*0.05]
        r_3=[min(min_1[2])-min(min_1[2])*0.05,max(max_1[2])+max((max_1[2]))*0.05]
        for i in range(12):
            fig.update_xaxes(range=r_1, row=1,col=i+1)
            fig.update_xaxes(range=r_2, row=2,col=i+1)
            fig.update_xaxes(range=r_3, row=3,col=i+1)
            fig.update_yaxes(range=r_1, row=1,col=i+1)
            fig.update_yaxes(range=r_2, row=2,col=i+1)
            fig.update_yaxes(range=r_3, row=3,col=i+1)
                

        fig.update_yaxes(title_text="Tensión (V)", row=1, col=1)
        fig.update_yaxes(title_text="Intensidad (A)", row=2, col=1)
        fig.update_yaxes(title_text="Potencia (kW)", row=3, col=1)
        fig.update_layout(            
            width=1350,
            height=650,
            font=dict(size=10),
            legend= {'itemsizing': 'constant'},
            legend_orientation="h",
            title={
                'text': A[n],
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'}) 
           
        pio.write_html(fig, file=path+'\R0_5\R0_'+A[n]+'.html', auto_open=False)