function[prx_i, pdl_iv, pdr_iv]=pot_intup(mi,nuec, Lci, Ptue)
% CALCULO DE LA POTENCIA DE Rx Interferente.
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
GeNB = 18;
mp=mi-1;
prx_i=zeros(nuec,mp);
for p1=1:mp % celdas interferentes
    for q1= 1:nuec %usuarios
    prx_i(q1,p1)= Ptue(q1,p1)+ GeNB -Lci(q1,p1);
    end 
end
M1= randn(nuec,mp); 
prx_int_des_l= M1+ prx_i;       % desvanecimiento lento
pdl_iv=10.^( prx_int_des_l/10);
rel_vol_int= sqrt(pdl_iv);
b_int= rel_vol_int/sqrt(pi./2);
vol_int_des_rl_v= raylrnd(b_int);  % desvanecimiento rapido
pdr_iv=((vol_int_des_rl_v).^2);
%prx_int1_des_rl=10*log10(pdr_iv);
end

