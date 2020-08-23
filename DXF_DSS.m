function [n_c,n_g]=DXF_DSS(caso,Gen_Max,P_c3,Curva_dem,dxf,directorio)
    cd(directorio)
    car=0;
    g=0;    
    % abre el fichero DSS
    fileID=fopen('Code/Cargas.dss','w');
    fileID2=fopen('Code/Lineas.dss','w');
    fileID3=fopen('Code/BusCoords.dat','w');
    fileID5=fopen('Code/LoadShapes.dss','w');
    fileID7=fopen('Code/CT.dss','w');
    fclose(fileID5);
    fclose(fileID);
    %Se define la curva de generación que se utiliza en los generadores
    fileID_3=fopen('Code/CurvasGeneracion.dss','w');  
    fprintf(fileID_3,"New Loadshape.CurvaGen npts=8760 interval=1\n");
    fprintf(fileID_3,"~ csvfile=%s\n","../Datos/CurvaGen_pu.csv");
    fclose(fileID_3);     
    flag=0;
    flag2=0;
    Buses1=0;
    f=3;
    for i = 1:dxf.ne    
        if(strcmp(dxf.entities(i).name,'LINE')==1)
           Nuevo=[dxf.entities(i).line(1),dxf.entities(i).line(2)] ; %%Crea un nuevo Bus
           Nueva=[dxf.entities(i).line,0]; %%Crea una nueva linea
           if(flag==0) 
               Buses1=Nuevo;
               Lineas1=Nueva;
           end            
           if(flag==1)
               Buses2=[Buses1;Nuevo];
               Buses1=Buses2;
               Lineas2=[Lineas1;Nueva];
               Lineas1=Lineas2;
           end
               Nuevo=[dxf.entities(i).line(3),dxf.entities(i).line(4)] ; %%Crea el segundo bus de la linea
               Buses2=[Buses1;Nuevo];
               Buses1=Buses2;          

          flag=1;   
        end   
        if(strcmp(dxf.entities(i).layer,'CT')==1 && strcmp(dxf.entities(i).name,'POINT')==1)
            CT=dxf.entities(i);        
        end
        if(strcmp(dxf.entities(i).layer,'Cargas')==1 && strcmp(dxf.entities(i).name,'POINT')==1)
             nombre=sprintf('%dc1',i);
             NCarga=[i,dxf.entities(i).point(1),dxf.entities(i).point(2),1]; %% 
             if(flag2==0)
               Loads=NCarga; %%Se crea una nueva carga definida con [i=numero de elemento, x,y, fases]
             end            
             if(flag2==1)
                Load2=[Loads;NCarga];
                Loads=Load2; 
             end
             flag2=1;   
        end 
        if(strcmp(dxf.entities(i).layer,'Cargas3f')==1 && strcmp(dxf.entities(i).name,'POINT')==1)
             nombre=sprintf('%dc3',i);
             NCarga=[i,dxf.entities(i).point(1),dxf.entities(i).point(2),3]; %%3 por trifásica
             if(flag2==0)
               Loads=NCarga; %%Se crea una nueva carga definida con [i=numero de elemento, x,y, fases]
             end            
             if(flag2==1)
                Load2=[Loads;NCarga];
                Loads=Load2; 
             end
             flag2=1;
        end
     end 
     Buses=unique(Buses1,'rows');
     Lines=unique(Lineas1,'rows');
     [r,c]=size(Buses);
     [r1,c1]=size(Loads);
     [r2,c2]=size(Lines);
     for i =1:r
         for k=1:r2
              if(Lines(k,1)==Buses(i,1)&& Lines(k,2)==Buses(i,2)&& Lines(k,5)==0) %%Para cada linea define los buses que forman la linea guardando los índices
                  Lines(k,5)=i;
              elseif(Lines(k,1)==Buses(i,1)&& Lines(k,2)==Buses(i,2))
                  Lines(k,6)=i;
              end
              if(Lines(k,3)==Buses(i,1)&& Lines(k,4)==Buses(i,2)&& Lines(k,5)==0)
                  Lines(k,5)=i;
              elseif(Lines(k,3)==Buses(i,1)&& Lines(k,4)==Buses(i,2))
                  Lines(k,6)=i;
              end          
         end
         if((abs(CT.point(1)-Buses(i,1))<=0.05) && (abs(CT.point(2)-Buses(i,2))<=0.05))
            fprintf(fileID7,"New Transformer.XFM1  Phases=3   Windings=2 Xhl=2.72\n");
            fprintf(fileID7,"~ wdg=1 bus=AT1      conn=Delta kv=15    kva=1260    %%r=0.635\n");
            fprintf(fileID7,"~ wdg=2 bus=bus%d     conn=Wye kv=0.400   \n",i);
         end
     end 
     for i =1:r 
         for j=1:r1
             if((abs(Loads(j,2)-Buses(i,1))<=0.005) && (abs(Loads(j,3)-Buses(i,2))<=0.005)) %%Define en cada bus si tiene una carga conectada escribiendo un 1 en la posición 3 del vector
                Buses(i,3)=Loads(j,4);            
             end             
         end
         Buses(i,4)=0; 
     end     
     for j=1:r2 %%Para cada linea si en alguno de sus buses hay una carga
         if Buses(Lines(j,5),3)~=0 || Buses(Lines(j,6),3)~=0
            if Buses(Lines(j,5),3)==1 || Buses(Lines(j,6),3)==1
                 if Buses(Lines(j,5),3)==1 
                     Buses(Lines(j,6),4)=Buses(Lines(j,6),4)+1;
                     nombre=sprintf('%dcM',Lines(j,5));
                     nombrebus2=sprintf("bus%d.%d",Lines(j,5),Buses(Lines(j,6),4));
                     nombrebus1=sprintf("bus%d.%d",Lines(j,6),Buses(Lines(j,6),4));            

                 elseif Buses(Lines(j,6),3)==1
                     Buses(Lines(j,5),4)=Buses(Lines(j,5),4)+1;
                     nombre=sprintf('%dcM',Lines(j,6));
                     nombrebus2=sprintf("bus%d.%d",Lines(j,6),Buses(Lines(j,5),4));
                     nombrebus1=sprintf("bus%d.%d",Lines(j,5),Buses(Lines(j,5),4));             
                 end
                 switch caso
                     case "25%"
                          if mod(j,4)==0     
                             PV_generator(nombrebus2,Gen_Max/1000);
                          end                          
                     case "50%"
                         if mod(j,2)==0     
                            PV_generator(nombrebus2,Gen_Max/1000);
                         end                         
                     case "75%"
                         if mod(j,4)~=0     
                            PV_generator(nombrebus2,Gen_Max/1000);
                         end                        
                     case "100%"                          
                            PV_generator(nombrebus2,Gen_Max/1000);
                                                   
                  end                   
                   NewLoad(nombre,nombrebus2,1,3,Curva_dem); 
                   f=1;      

            elseif Buses(Lines(j,5),3)==3 || Buses(Lines(j,6),3)==3
                 if Buses(Lines(j,5),3)==3 
                     Buses(Lines(j,6),4)=3;
                     nombre=sprintf('%dcT',Lines(j,5));
                     nombrebus2=sprintf("bus%d",Lines(j,5));
                     nombrebus1=sprintf("bus%d",Lines(j,6));            

                 elseif Buses(Lines(j,6),3)==3
                     Buses(Lines(j,5),4)=3;
                     nombre=sprintf('%dcT',Lines(j,6));
                     nombrebus2=sprintf("bus%d",Lines(j,6));
                     nombrebus1=sprintf("bus%d",Lines(j,5));             
                 end
                  switch caso
                     case "25%"
                          if mod(j,4)==0     
                             PV_generator(nombrebus2,Gen_Max/1000);
                             g=g+1;
                          end                         
                     case "50%"
                         if mod(j,2)==0     
                            PV_generator(nombrebus2,Gen_Max/1000);
                            g=g+1;
                         end                         
                     case "75%"
                         if mod(j,4)~=0     
                            PV_generator(nombrebus2,Gen_Max/1000);
                            g=g+1;
                         end                        
                     case "100%"                          
                            PV_generator(nombrebus2,Gen_Max/1000);
                            g=g+1;
                  end       
                        
                    NewLoad(nombre,nombrebus2,3,P_c3,Curva_dem); %Se supone que cada piso tiene contratada 3.5 kW y hay 10 casas por bloque
                    car=car+1;
                    f=3;
            end
        else
         nombrebus2=sprintf("bus%d",Lines(j,6));
         nombrebus1=sprintf("bus%d",Lines(j,5));
         f=3;
        end

         nombrelinea=sprintf("line%d",j);
         d=sqrt((Lines(j,1)-Lines(j,3))^2+(Lines(j,2)-Lines(j,4))^2);
         fprintf(fileID2,"New Line.%s\tPhases=%d\tBus1=%s\tBus2=%s\tGeometry=4_240_AL\tLength=%f\tunits=m\n",nombrelinea,f,nombrebus1,nombrebus2,d);

     end 
     for i=1:r
         fprintf(fileID3,"bus%d\t%f\t%f\n",i,Buses(i,1),Buses(i,2)); %% Crea el fichero con las coordenadas de los puntos     
     end
     fclose(fileID2);
     fclose(fileID3);
     fclose(fileID7);
    n_c=car;
    n_g=g;
end

 
 
 
         
  

       
 
 
     
   
    
