function OpenDSS_R (caso, elementos)
    close all;
    [DSSStartOK, DSSObj, DSSText] = DSSStartup;
    if DSSStartOK
        compile_file=strcat(pwd,"\Code\Master.dss");
        comando=sprintf('Compile (%s)',compile_file);
        DSSText.Command =comando;
        DSSCircuit = DSSObj.ActiveCircuit;
        DSSSolution=DSSCircuit.Solution;
        DSSText.Command='Redirect CircuitPlottingScripts.dss';
        [f,c]=size(elementos);
        %Se crean los monitores
        for i=1:f
            com1=sprintf('New Monitor.%sP element=Line.%s terminal=1 mode=1 ppolar=0',elementos(i),elementos(i));
            com2=sprintf('New Monitor.%sV element=Line.%s terminal=1 mode=0',elementos(i),elementos(i));
            DSSText.Command=com1;
            DSSText.Command=com2;
        end
    DSSSolution.Solve;
    %Se realiza el plot en OpenDSS para comprobar los resultados
    DSSText.Command='Plot monitor object=line1P channels=(1)';
    DSSText.Command='Plot monitor object=line1V channels=(1)';
    DSSText.Command='Plot monitor object=line1V channels=(9)';
    DSSText.Command='Plot monitor object=line1V channels=(2)';
    DSSText.Command='Plot monitor object=line1V channels=(10)';
    DSSMon=DSSCircuit.Monitors;
    
        for i=1:f
            name_c=sprintf('%sV',elementos(i));
            DSSMon.name=name_c;
            V1(i,:) = ExtractMonitorData(DSSMon,1,400);
            I1(i,:) = ExtractMonitorData(DSSMon,9,20);
            Va1(i,:)= ExtractMonitorData(DSSMon,2,1);
            Ia1(i,:)= ExtractMonitorData(DSSMon,10,1);
            name_c=sprintf('%sP',elementos(i));
            DSSMon.name=name_c;
            P1(i,:)= ExtractMonitorData(DSSMon,1,10);
            %Se cambia de signo las variables para que tengan el mismo
            %sentido
            if(sum(P1(i,:))<0)
                P1(i,:)=-P1(i,:);
                Ia1(i,:)= Ia1(i,:)-180; 
            end
            for x=1:8760
                if (Ia1(i,x)<0)
                    Ia1(i,x)=360+Ia1(i,x);
                end
                if (Va1(i,x)<0)
                    Va1(i,x)=360+Va1(i,x);
                end
            end
            
           
            t = ExtractMonitorData(DSSMon,0,3600.0);    
        end
        
        [n,m]=size(elementos)
         header = elementos';
         c=cell(8761,n);
         d=cell(8761,n);
         e=cell(8761,n);
         f=cell(8761,n);
         g=cell(8761,n);
         c(1,:) = cellstr(header);
         c(2:8761,:) = num2cell(V1'*400);
         d(1,:) =cellstr(header);
         d(2:8761,:) =num2cell(I1'*20);
         e(1,:) = cellstr(header);
         e(2:8761,:) = num2cell(P1'*10);
         f(1,:) = cellstr(header);
         f(2:8761,:) = num2cell(Va1'*1);
         g(1,:) = cellstr(header);
         g(2:8761,:) = num2cell(Ia1'*1);
         filename = strcat(pwd,"\Resultados\",caso,".xlsx");
         xlswrite(filename,c,1);        
         xlswrite(filename,d,2);         
         xlswrite(filename,e,3);
         xlswrite(filename,f,4);
         xlswrite(filename,g,5);
    else
        a='DSS Did Not Start';
        disp(a)
    end
end