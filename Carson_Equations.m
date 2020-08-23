d=17.2; %%mm
R_dc=0.125; %%Ohm/km
GMR=d/2*0.7788 %%mm
R_dc_m=R_dc*1.60934 %%Paso a Ohm/mile 
E=1.4240*(10^(-2)) %%mile/nF
GMR_m=GMR* 0.00328084 %%Paso a ft.
Pos=[0+1j*70, 3+1j*70, 0+1j*73, 3+1j*73] %%cm
for i=1:4 
    for j=1:4
        if i==j
            D_t(i,j)=GMR_m;            
        else
            D_t(i,j)=abs(Pos(i)-Pos(j));
        end
        S_t(i,j)=abs(Pos(i)-conj(Pos(j)));      
    end
end
D=D_t*0.0328084 %%Paso de cm a feet
S=S_t*0.0328084
for i=1:4
    for j=1:4
        if i==j
            M(i,j)=R_dc_m+0.07934+1i*0.10112*(log(1/GMR_m)+7.33202); %%Para frecuencia 60 Hz          
        else
            M(i,j)=0.07934+1i*0.10112*(log(1/D(i,j))+7.33202);
        end
        P(i,j)=(1/(2*pi()*E))*log(S(i,j)/D(i,j));
    end
end
P
P_2=P/1.60934
C_2=inv(P*(1.60934/1000))
M_2=M/1.60934
M

