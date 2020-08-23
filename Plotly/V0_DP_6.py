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
def Plot_VR0(df,A,B,path):
    os.makedirs(path+'\R0_VIP_6', exist_ok=True)
    meses=[]
    legend_g=[]
    for x in range(0,12):
        meses.append(datetime(2017,(x+1),1,0).month)

    for i in range(0,len(A)):
        for n in range(1,len(B)):
            legend_g.append(str(A[i]+"("+B[n]+")"))
    
    fig = make_subplots(rows=3, cols=12,
                        shared_yaxes=True,
                        vertical_spacing=0.08,
                        horizontal_spacing=0.01,
                        column_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        x_title="Variación porcentual respecto a un escenario sin generación fotovoltaica (%)",
                        row_titles=("Tensión","Intensidad","Potencia"),
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
            for m in range(0,12): 
                x11=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Tensión"].to_list() 
                x01=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Tensión"].to_list() 
                x12=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Intensidad"].to_list() 
                x02=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Intensidad"].to_list() 
                x13=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Potencia"].to_list() 
                x03=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Potencia"].to_list() 
                x21=[] 
                x22=[] 
                x23=[]              
                for t in range(len(x11)):
                    x1=(x11[t]-x01[t])*100/x01[t]
                    x21.append(x1)
                    x2=(x12[t]-x02[t])*100/x02[t]
                    x22.append(x2)
                    x3=(x13[t]-x03[t])*100/x03[t]
                    x23.append(x3)
                xi1.append(min(x21))
                xi2.append(min(x22))
                xi3.append(min(x23))
                xs1.append(max(x21))
                xs2.append(max(x22))
                xs3.append(max(x23))
                etiqueta=legend_g[n*(len(B)-1)+s]   
                dens=ff.create_distplot([x21],[etiqueta],bin_size=0.1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                fig.add_trace(dens['data'][0],1,m+1)  
                ys1.append(max(dens['data'][0]['y']))
                dens=ff.create_distplot([x22],[etiqueta],bin_size=5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                fig.add_trace(dens['data'][0],2,m+1)
                ys2.append(max(dens['data'][0]['y']))
                if m!=11:                
                    dens=ff.create_distplot([x23],[etiqueta],bin_size=5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                    fig.add_trace(dens['data'][0],3,m+1)
                    ys3.append(max(dens['data'][0]['y']))
        fig.update_traces(showlegend=False)   
    for n in range(0,len(A)):       
        for s in range(0,len(B)-1):
            m=11
            x13=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Potencia"].to_list() 
            x03=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Potencia"].to_list() 
            x23=[]              
            for t in range(len(x13)):               
                x3=(x13[t]-x03[t])*100/x03[t]
                x23.append(x3)       
            xi3.append(min(x23))            
            xs3.append(max(x23))
            etiqueta=legend_g[n*(len(B)-1)+s]   
            dens=ff.create_distplot([x23],[etiqueta],bin_size=5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
            fig.add_trace(dens['data'][0],3,m+1)
            ys3.append(max(dens['data'][0]['y']))   
    
    m_X1=[min(xi1)-0.05*min(xi1),max(xs1)+0.05*max(xs1)]
    m_X2=[min(xi2)-0.05*min(xi2),max(xs2)+0.05*max(xs2)]
    m_X3=[min(xi3)-0.05*min(xi3),max(xs3)+0.05*max(xs3)]
    m_Y1=[0,max(ys1)+0.05*max(ys1)]
    m_Y2=[0,max(ys2)+0.05*max(ys2)]
    m_Y3=[0,max(ys3)+0.05*max(ys3)]
    fig.update_xaxes(range=m_X1,row=1)   
    fig.update_xaxes(range=m_X2,row=2)  
    fig.update_xaxes(range=m_X3,row=3)  
    fig.update_yaxes(range=m_Y1,nticks=10,col=1,row=1)
    fig.update_yaxes(range=m_Y2,nticks=10,col=1,row=2)
    fig.update_yaxes(range=m_Y3,nticks=10,col=1,row=3)      
    fig.update_layout(      
        width=1350,
        height=650,
        font=dict(size=10))       
        
    pio.write_html(fig, file=path+'\R0_VIP_6.html', auto_open=True) 

          
    for n in range(0,len(A)): 
        fig = make_subplots(rows=3, cols=12,
                        shared_yaxes=True,
                        vertical_spacing=0.08,
                        horizontal_spacing=0.01,
                        column_titles=("Ene.","Feb.","Mar.","Abr.","May.","Jun.","Jul.","Ago.","Sep.","Oct.","Nov.","Dic."),
                        row_titles=("Tensión","Intensidad","Potencia"),
                        x_title="Variación porcentual respecto a un escenario sin generación fotovoltaica (%)",      
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
            for m in range(0,12): 
                x11=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Tensión"].to_list() 
                x01=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Tensión"].to_list() 
                x12=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Intensidad"].to_list() 
                x02=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Intensidad"].to_list() 
                x13=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Potencia"].to_list() 
                x03=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Potencia"].to_list() 
                x21=[] 
                x22=[] 
                x23=[]              
                for t in range(len(x11)):
                    x1=(x11[t]-x01[t])*100/x01[t]
                    x21.append(x1)
                    x2=(x12[t]-x02[t])*100/x02[t]
                    x22.append(x2)
                    x3=(x13[t]-x03[t])*100/x03[t]
                    x23.append(x3)
                xi1.append(min(x21))
                xi2.append(min(x22))
                xi3.append(min(x23))
                xs1.append(max(x21))
                xs2.append(max(x22))
                xs3.append(max(x23))
                etiqueta=legend_g[n*(len(B)-1)+s]   
                dens=ff.create_distplot([x21],[etiqueta],bin_size=0.1,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                fig.add_trace(dens['data'][0],1,m+1)  
                ys1.append(max(dens['data'][0]['y']))
                dens=ff.create_distplot([x22],[etiqueta],bin_size=5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                fig.add_trace(dens['data'][0],2,m+1)
                ys2.append(max(dens['data'][0]['y']))
                if m!=11:                
                    dens=ff.create_distplot([x23],[etiqueta],bin_size=5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
                    fig.add_trace(dens['data'][0],3,m+1)
                    ys3.append(max(dens['data'][0]['y']))
        fig.update_traces(showlegend=False)   
          
        for s in range(0,len(B)-1):
            m=11
            x13=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[s+1]+")\'"))["Potencia"].to_list() 
            x03=df.query("Mes=="+str(meses[m])+" and "+"Linea=="+str("\'"+A[n]+"("+B[0]+")\'"))["Potencia"].to_list() 
            x23=[]              
            for t in range(len(x13)):               
                x3=(x13[t]-x03[t])*100/x03[t]
                x23.append(x3)       
            xi3.append(min(x23))            
            xs3.append(max(x23))
            etiqueta=legend_g[n*(len(B)-1)+s]   
            dens=ff.create_distplot([x23],[etiqueta],bin_size=5,show_hist=False,show_rug=False, colors=[px.colors.qualitative.Prism[((s+(len(B)-1)*n)*2)%11]], histnorm='probability density')              
            fig.add_trace(dens['data'][0],3,m+1)
            ys3.append(max(dens['data'][0]['y']))  
           
          
        m_X1=[min(xi1)-0.05*min(xi1),max(xs1)+0.05*max(xs1)]
        m_X2=[min(xi2)-0.05*min(xi2),max(xs2)+0.05*max(xs2)]
        m_X3=[min(xi3)-0.05*min(xi3),max(xs3)+0.05*max(xs3)]
        m_Y1=[0,max(ys1)+0.05*max(ys1)]
        m_Y2=[0,max(ys2)+0.05*max(ys2)]
        m_Y3=[0,max(ys3)+0.05*max(ys3)]
        fig.update_xaxes(range=m_X1,row=1)   
        fig.update_xaxes(range=m_X2,row=2)  
        fig.update_xaxes(range=m_X3,row=3)  
        fig.update_yaxes(range=m_Y1,nticks=10,col=1,row=1)
        fig.update_yaxes(range=m_Y2,nticks=10,col=1,row=2)
        fig.update_yaxes(range=m_Y3,nticks=10,col=1,row=3)         
            
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
        pio.write_html(fig, file=path+'\R0_VIP_6\R0_'+A[n]+'.html', auto_open=False) 
           