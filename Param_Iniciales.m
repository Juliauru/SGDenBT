function [Gen_Max,Curva_demanda,CurvaGen] = Param_Iniciales(fich_gen)
%Param_radiacion: Trata las curvas de radiación y de generación

%Se utliza la curva de generación horaria para realizar una curva de
%potencia generada pu
    fileID_2=fopen(fich_gen,'r');
    CurvaGen=fscanf(fileID_2,'%f',[1 Inf]);
    fclose(fileID_2);
    Gen_Max=max(CurvaGen);
    CurvaGen_pu=CurvaGen(:)/Gen_Max;
    csvwrite('Datos/CurvaGen_pu.csv',CurvaGen_pu); 
    
%Se lee la curva de demandas de REE
    fileID_4=fopen('Datos/DemandasYear.csv','r');
    Curva_demanda=fscanf(fileID_4,'%f',[1 Inf]);
    fclose(fileID_4);    
end

