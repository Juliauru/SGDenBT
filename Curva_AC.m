%Balance de potencias desde el punto de vista del CT
function [Curva_AC] = Curva_AC(n_c,n_g,Curva_D,P,CurvaGen)
    CurvaDem=Curva_D*P*1000;
    Curva_AC=(n_c*CurvaDem(1,1:8760))-(n_g*CurvaGen(1,1:8760));        
end

