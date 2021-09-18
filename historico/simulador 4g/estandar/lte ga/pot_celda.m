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

%% Calculo de las potencias en cada celda 

function[prx, pdl, pdr]=pot_celda(m, nuec, Gc, Lc, ptx)
% % Celda 
 prx= 10*log10(ptx)+Gc(:,m)-Lc(:,m);
 % Potencia incluyendo el desvanecimiento lento y rapido
 N= 4*randn(nuec,1);
 pdl= N+ prx;    % desvanecimiento lento
 prx_des_lv= 10.^(pdl./10);
 rel_vol= sqrt(prx_des_lv);
 b= rel_vol/sqrt(pi./2);
 prx_des_rl_v= raylrnd(b);
 pdr=20*log10(prx_des_rl_v);
end
