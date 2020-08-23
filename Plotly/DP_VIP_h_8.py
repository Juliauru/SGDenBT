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

#Leo datos
def Plot_V_h(df,A,B,path):
    os.makedirs(path+'\R0_VIP_h_8', exist_ok=True)
    meses=[]
    legend_g=[]
    inicio = datetime(2017,1,1,0)
    fin = datetime(2017,12,31,23) 
    lista_fechaH= [(inicio + timedelta(days=d/24)).strftime("%H") for d in range(24)]   
    for i in range(0,len(A)):
        for n in range(1,len(B)):
            legend_g.append(str(A[i]+"("+B[n]+")"))
    
    fig = make_subplots(rows=4, cols=6,
                        shared_yaxes=True,
                        vertical_spacing=0.08,
                        horizontal_spacing=0.01,                        
                        x_title="Variación porcentual respecto a una penetración del 0%",
                        subplot_titles=lista_fechaH,
                        y_title="Densidad de probabilidad"                                            
                    )   
    xi1=[]
    xs1=[]
    ys1=[]    
    xi2=[]
    xs2=[]
    ys2=[]  
    xi3=[]
    xs3=[]
    ys3=[]      
    for n in range(0,len(A)):       
        for s in range(0,len(B)-1):
            for m in range(0,23): 
                x11=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Tensión"].to_list() 
                x01=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Tensión"].to_list() 
                x21=[]                       
                for t in range(len(x11)):
                    x1=(x11[t]-x01[t])*100/x01[t]
                    x21.append(x1)                    
                xi1.append(min(x21))                
                xs1.append(max(x21))                
                etiqueta=legend_g[n*(len(B)-1)+s]   
                dens=ff.create_distplot([x21],[etiqueta],bin_size=0.1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                fig.append_trace(dens['data'][0],(m//6)+1,(m%6)+1) 
                ys1.append(max(dens['data'][0]['y'])) 
    fig.update_traces(showlegend=False) 
    for n in range(0,len(A)):       
        for s in range(0,len(B)-1):
            m=23
            x11=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Tensión"].to_list() 
            x01=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Tensión"].to_list() 
            x21=[]                       
            for t in range(len(x11)):
                x1=(x11[t]-x01[t])*100/x01[t]
                x21.append(x1)                    
            xi1.append(min(x21))                
            xs1.append(max(x21))                
            etiqueta=legend_g[n*(len(B)-1)+s]   
            dens=ff.create_distplot([x21],[etiqueta],bin_size=0.1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
            fig.append_trace(dens['data'][0],(m//6)+1,(m%6)+1) 
            ys1.append(max(dens['data'][0]['y']))               

    m_X1=[min(xi1)-0.05*min(xi1),max(xs1)+0.05*max(xs1)]    
    m_Y1=[0,max(ys1)+0.05*max(ys1)]   
    fig.update_xaxes(range=m_X1,ticksuffix="%") 
    fig.update_yaxes(range=m_Y1,nticks=5)
     
    fig.update_layout(      
        width=1350,
        height=650,
        font=dict(size=10))       
        
    pio.write_html(fig, file=path+'\R0_VIP_h_8.html', auto_open=True) 

    for n in range(0,len(A)): 
        fig = make_subplots(rows=4, cols=6,
                                shared_yaxes=True,
                                vertical_spacing=0.08,
                                horizontal_spacing=0.01,                        
                                x_title="Variación porcentual respecto a una penetración del 0%",
                                subplot_titles=lista_fechaH,
                                y_title="Densidad de probabilidad"                                            
                            )   
        xi1=[]
        xs1=[]
        ys1=[]    
        xi2=[]
        xs2=[]
        ys2=[]  
        xi3=[]
        xs3=[]
        ys3=[]      
              
        for s in range(0,len(B)-1):
            for m in range(0,23): 
                x11=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Tensión"].to_list() 
                x01=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Tensión"].to_list() 
                x21=[]                       
                for t in range(len(x11)):
                    x1=(x11[t]-x01[t])*100/x01[t]
                    x21.append(x1)                    
                xi1.append(min(x21))                
                xs1.append(max(x21))                
                etiqueta=legend_g[n*(len(B)-1)+s]   
                dens=ff.create_distplot([x21],[etiqueta],bin_size=0.1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                fig.append_trace(dens['data'][0],(m//6)+1,(m%6)+1) 
                ys1.append(max(dens['data'][0]['y']))
        fig.update_traces(showlegend=False)                
        for s in range(0,len(B)-1):
            m=23
            x11=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Tensión"].to_list() 
            x01=df.query("Hora=="+str("\'"+lista_fechaH[m]+"\'")+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Tensión"].to_list() 
            x21=[]                       
            for t in range(len(x11)):
                x1=(x11[t]-x01[t])*100/x01[t]
                x21.append(x1)                    
            xi1.append(min(x21))                
            xs1.append(max(x21))                
            etiqueta=legend_g[n*(len(B)-1)+s]   
            dens=ff.create_distplot([x21],[etiqueta],bin_size=0.1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
            fig.append_trace(dens['data'][0],(m//6)+1,(m%6)+1) 
            ys1.append(max(dens['data'][0]['y']))    
    
        m_X1=[min(xi1)-0.05*min(xi1),max(xs1)+0.05*max(xs1)]    
        m_Y1=[0,max(ys1)+0.05*max(ys1)]   
        fig.update_xaxes(range=m_X1,ticksuffix="%") 
        fig.update_yaxes(range=m_Y1,nticks=5)
     
        fig.update_layout(      
            width=1350,
            height=650,
            font=dict(size=10),
            title={
                'text': A[n],
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})     
                
        pio.write_html(fig, file=path+'\R0_VIP_h_8\R0_h_'+A[n]+'.html', auto_open=False) 