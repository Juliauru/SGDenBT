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
def Plot_V230_DP(df,A,B,path):       
    os.makedirs(path+'\Densidad_Probabilidad_3', exist_ok=True)
    legend_g=[]
    meses=[]
    for x in range(0,12):
        meses.append(datetime(2017,(x+1),1,0).month)

    for i in range(0,len(A)):
        for n in range(0,len(B)):    
            legend_g.append(str(A[i]+"("+ B[n]+ ")"))   
  
    #Se crean los plots
    fig = make_subplots(rows=3, cols=4,
                        shared_yaxes=True,
                        vertical_spacing=0.1,
                        horizontal_spacing=0.02,
                        subplot_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        x_title="Variación porcentual de la tensión respecto a Vbase=230V",
                        y_title="Densidad de probabilidad"
                    )
    #Se añaden los plots y se ajustan los ejes respecto a los valores mínimos y máximos del conjunto de subplots
    xi=[]
    xs=[]
    yi=[]
    ys=[]    
    for n in range(0,len(A)):       
        for s in range(0,len(B)):            
            for m in range(0,11):  
                               
                x=((df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"]-230)*100)/230 
                etiqueta=legend_g[n*len(B)+s]  
                dens=ff.create_distplot([x],[etiqueta],bin_size=1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+len(B)*n)*2)%11]],histnorm='probability density')    
                fig.append_trace(dens['data'][0],row=(m//4)+1,col=(m%4)+1) 
                mi_1=min(x)
                ma_1=max(x)
                xi.append(mi_1)
                xs.append(ma_1)
                mi_1=min(dens['data'][0]['y'])
                ma_1=max(dens['data'][0]['y'])
                yi.append(mi_1)
                ys.append(ma_1) 
    fig.update_traces(showlegend=False) 
    for n in range(0,len(A)):       
        for s in range(0,len(B)):            
            m=11                               
            x=((df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"]-230)*100)/230 
            etiqueta=legend_g[n*len(B)+s]  
            dens=ff.create_distplot([x],[etiqueta],bin_size=1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+len(B)*n)*2)%11]],histnorm='probability density')    
            fig.append_trace(dens['data'][0],row=(m//4)+1,col=(m%4)+1) 
            mi_1=min(x)
            ma_1=max(x)
            xi.append(mi_1)
            xs.append(ma_1)
            mi_1=min(dens['data'][0]['y'])
            ma_1=max(dens['data'][0]['y'])
            yi.append(mi_1)
            ys.append(ma_1) 

    m_X=[min(xi)-0.05*min(xi),max(xs)+0.05*max(xs)]
    print(len(x))
    m_Y=[0,max(ys)+0.05*max(ys)]
    fig.update_xaxes(range=m_X,nticks=11,ticksuffix="%")
    fig.update_yaxes(range=m_Y,nticks=10) 
       
    fig.update_layout(      
        width=1350,
        height=650,
        font=dict(size=10),    
         
    )
    print(len(fig.data))
    pio.write_html(fig, file=path+'\Densidad_Probabilidad_3.html', auto_open=True) 

    #Se repite lo anterior para cada una de las gráficas por separado en un '.html'
    
    for n in range(0,len(A)): 
        fig = make_subplots(rows=3, cols=4,
                        shared_yaxes=True,
                        vertical_spacing=0.1,
                        horizontal_spacing=0.02,
                        subplot_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        x_title="Variación porcentual de la tensión respecto a Vbase=230V",
                        y_title="Densidad de probabilidad"
                    )   
        xi=[]
        xs=[]
        yi=[]
        ys=[]   
        for s in range(0,len(B)):
            for m in range(0,11):                                      
                x=((df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"]-230)*100)/230
                etiqueta=legend_g[n*len(B)+s]                     
                dens=ff.create_distplot([x],[etiqueta],bin_size=0.5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+len(B)*n)*2)%11]], histnorm='probability density')              
                fig.append_trace(dens['data'][0],row=(m//4)+1,col=(m%4)+1)  
                mi_1=min(x)
                ma_1=max(x)
                xi.append(mi_1)
                xs.append(ma_1)
                mi_1=min(dens['data'][0]['y'])
                ma_1=max(dens['data'][0]['y'])
                yi.append(mi_1)
                ys.append(ma_1)
                '''area=0      
                for i in range(int(len(dens['data'][0]['y'])-1)):
                    menor_y=min(dens['data'][0]['y'][i],dens['data'][0]['y'][i+1])
                    mayor_y=max(dens['data'][0]['y'][i],dens['data'][0]['y'][i+1])
                    menor_x=min(dens['data'][0]['x'][i],dens['data'][0]['x'][i+1])
                    mayor_x=max(dens['data'][0]['x'][i],dens['data'][0]['x'][i+1])
                    area=((mayor_x-menor_x)*(mayor_y-menor_y)/2)+(mayor_x-menor_x)*menor_y+area                
                print(area)'''
        fig.update_traces(showlegend=False) 
        for s in range(0,len(B)):
            m=11                                     
            x=((df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s]+")\'"))["Tensión"]-230)*100)/230
            etiqueta=legend_g[n*len(B)+s]                     
            dens=ff.create_distplot([x],[etiqueta],bin_size=0.5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+len(B)*n)*2)%11]], histnorm='probability density')              
            fig.append_trace(dens['data'][0],row=(m//4)+1,col=(m%4)+1)  
            mi_1=min(x)
            ma_1=max(x)
            xi.append(mi_1)
            xs.append(ma_1)
            mi_1=min(dens['data'][0]['y'])
            ma_1=max(dens['data'][0]['y'])
            yi.append(mi_1)
            ys.append(ma_1)
            '''area=0      
            for i in range(int(len(dens['data'][0]['y'])-1)):
                menor_y=min(dens['data'][0]['y'][i],dens['data'][0]['y'][i+1])
                mayor_y=max(dens['data'][0]['y'][i],dens['data'][0]['y'][i+1])
                menor_x=min(dens['data'][0]['x'][i],dens['data'][0]['x'][i+1])
                mayor_x=max(dens['data'][0]['x'][i],dens['data'][0]['x'][i+1])
                area=((mayor_x-menor_x)*(mayor_y-menor_y)/2)+(mayor_x-menor_x)*menor_y+area                
            print(area)'''
       
        m_X=[min(xi)-0.05*min(xi),max(xs)+0.05*max(xs)]
        print(len(x))
        m_Y=[0,max(ys)+0.05*max(ys)]
        fig.update_xaxes(range=m_X,nticks=11,ticksuffix="%")
        fig.update_yaxes(range=m_Y,nticks=10)
        fig.update_layout(      
        width=1350,
        height=650,
        font=dict(size=10),  
        title={
            'text': A[n],
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',},)            
        pio.write_html(fig, file=path+'\Densidad_Probabilidad_3\VT_'+A[n]+'.html', auto_open=False) 
