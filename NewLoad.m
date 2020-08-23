function NewLoad(nombre,nombrebus2,fases,potencia,Curva)
%Se abren los identificadores de fichero
    fileID_5=fopen('Code/LoadShapes.dss','a');
    fileID_1=fopen('Code/Cargas.dss','a');

    Curva2=Curva;
    nombrearchivo=sprintf("CurvasCarga/Loadshape%s.csv",nombre); %% Se define la curva de cargas
    nombrecurva=sprintf("Shape%s",nombre);            
    for i=1:8760                 
    Curva2(i)=random('Normal',Curva(i),0.05);
    end
    Curva3=Curva2';
    csvwrite(nombrearchivo,Curva3(:,1));
    fprintf(fileID_5,"New Loadshape.Shape%s npts=8760 interval=1\n",nombre);
    fprintf(fileID_5,"~ csvfile=../%s\n",nombrearchivo);
    fprintf(fileID_1,"New Load.%s\tBus1=%s\tPhases=%d\tConn=Wye\tModel=1\tkV=0.4\tkW=%d\tpf=0.92\tyearly=%s\n",nombre,nombrebus2,fases,potencia,nombrecurva);
    fclose(fileID_1);
    fclose(fileID_5);
end

