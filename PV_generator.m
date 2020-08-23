function  PV_generator(bus,potencia)
    num=sscanf(bus,"bus%d"); 
    fileID_3=fopen('Code/CurvasGeneracion.dss','a');  
    fprintf(fileID_3,"New generator.gen%d bus1=%s kV=0.4 kW=%f pf=1 yearly=CurvaGen\n",num,bus,potencia);
    fclose(fileID_3);
end
