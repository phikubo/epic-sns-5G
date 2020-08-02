% Simulador Básico a Nivel de Sistema para LTE.
% Licencia academica, no comercial.
% Autor: Claudia Shirley Paz Arteaga, Eileen Johana Martinez Gómez
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2014

% Simulador Básico a Nivel de Sistema para LTE con Planificadores de Recursos Radio Integrados.
% Licencia academica, no comercial.
% Autor: Darío Giraldo Medina, Diego Fernando Uribe Ante
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2015

% Simulador Básico a Nivel de Sistema para LTE con Planificadores de Recursos Radio Integrados y Técnicas de Reúso de Frecuencia.
% Licencia academica, no comercial.
% Autor: María Manuela Silva Zambrano, Valentina Giselle Moreno Parra
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2015

%%

% CALCULO DE LA POTENCIA DE Rx Interferente.

function[prx_i, pdl_iv, pdr_iv]=pot_int(mi,nuec, Gci, Lci, pt)

mp=mi-1;
prx_i=zeros(nuec,mp);
for p1=1:mp % celdas interferentes
    for q1= 1:nuec %usuarios
    prx_i(q1,p1)= 10*log10(pt)+Gci(q1,p1)-Lci(q1,p1);
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