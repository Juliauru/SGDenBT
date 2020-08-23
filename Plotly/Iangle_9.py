# mymod4.py
import os
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
from datetime import datetime,timedelta
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
def Plot_Iangle(df,A,B,path):       
    os.makedirs(path+'\Iangle_9', exist_ok=True)
    legend_g=[]
    meses=[]
    for x in range(0,12):
        meses.append(datetime(2017,(x+1),1,0).month)

    for i in range(0,len(A)):
        for n in range(0,len(B)):    
            legend_g.append(str(A[i]+"("+ B[n]+ ")"))   
  
    #Se crean los plots
    for n in range(0,len(A)): 
        fig = make_subplots(rows=3, cols=4,
                            shared_yaxes=True,
                            vertical_spacing=0.1,
                            horizontal_spacing=0.02,
                            subplot_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                            x_title="Irradiancia (W/m²)",
                            y_title="Intensidad (A)"
                    )
    #Se añaden los plots y se ajustan los ejes respecto a los valores mínimos y máximos del conjunto de subplots
        min_1=[]
        max_1=[]      
        for s in range(0,len(B)):
            for m in range(0,12):              
                    fig.add_trace(
                        go.Scattergl(
                            mode='markers',                      
                            showlegend=False,
                            legendgroup=legend_g[s+len(B)*n],
                            marker=dict(color=(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Vangle"]-df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Iangle"]),showscale=True, coloraxis = "coloraxis",size=4,
                                        ),
                            name=legend_g[s+len(B)*n],
                            x=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Radiación"],
                            y=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Intensidad"],

                        ),
                        row=(m//4)+1, 
                        col=(m%4)+1
                    )  
                    f=min(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Intensidad"])
                    ff=max(df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Intensidad"]) 
                    min_1.append(f)              
                    max_1.append(ff)        
                
    
        F_t=[]
        for f in range(0,len(B)):
            F=[False]*len(fig.data)
            F[(12*f):(12*(f+1))]=[True]*12  
            F_t.append(F) 
        botones=[]
        for  t in range(0,len(B)):
            d=dict(label=B[t],
                            method="update",
                            args=[{"visible": F_t[t]},
                ])
            botones.append(d) 
        d=dict(label="All",
                            method="update",
                            args=[{"visible": [True]*len(fig.data)},
            ])
        botones.append(d)   
        fig.update_xaxes(range=[0,1400])
        fig.update_yaxes(range=[min(min_1)-0.05*min(min_1),max(max_1)+(0.05*max(max_1))]) 
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
                    buttons=botones,
                )
            ])   
        fig.update_layout(      
            width=1350,
            height=650,
            font=dict(size=10),
            coloraxis= {'colorscale':'Portland','cmin':0,'cmax':180,'colorbar.title.text':'Desfase I-V','colorbar.ticksuffix':'°'},
            legend= {'itemsizing': 'constant',
            },
            title={
                'text': A[n],
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
           
            )       
       
        print(len(fig.data))
        pio.write_html(fig, file=path+'\Iangle_9\Ia_'+A[n]+'.html', auto_open=False) 

    