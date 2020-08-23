clc; close all;
%% Godella 
elementos=["line53";"line46";"line43";"line44";"line45";"line48";"line28";"line75";"line71";"line17"];
%% Benimamet: 
%%elementos=["line1";"line2";"line4";"line41";"line69";"line116";"line221";"line239";"line266";
%%           "line139";"line211";"line226";"line230";"line233";"line188";"line155"];
%% Estocolmo: 
%%elementos=["line6";"line20";"line56";"line151";"line234";"line238";"line240";"line244";"line194";"line73";"line76"];
casos=["0%";"25%";"50%";"75%";"100%"];
% crea carpetas contenedoras
mkdir('CurvasCarga');
mkdir('Code');
mkdir('Resultados');
[Gen_Max,Curva_dem,Curva_gen]=Param_Iniciales('Datos/CurvaGen_L.csv');
dxf=Leer_DXF('Godella.dxf');
directorio=pwd;
[n,m]=size(casos);
for i=1:n
[n_c,n_g]=DXF_DSS(casos(i),Gen_Max,25,Curva_dem,dxf,directorio); %Son 10 pisos por bloque y cada carga 2.5 kW
OpenDSS_R(casos(i),elementos);
A(i,:)=Curva_AC(n_c,n_g,Curva_dem,25,Curva_gen);
end
[n,m]=size(casos)
header = casos';
c=cell(8761,n);
c(1,:) = cellstr(header);
c(2:8761,:) = num2cell(A'); 
filename = strcat(pwd,"\Resultados\Curvas_AC.xlsx");
xlswrite(filename,c,1);        


