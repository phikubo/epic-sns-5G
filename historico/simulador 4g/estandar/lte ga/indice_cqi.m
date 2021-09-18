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

%% Asignación del CQI 

function[cqi]=indice_cqi(nuec,sinr)

cqi=zeros(nuec,4);
tabla_itbs= xlsread('CQI.xls');

for a=1:nuec
       for b=1:4
             for i=2:16
             if(sinr(a,b)>22.7)
             cqi(a,b)=15;
             elseif (sinr(a,b)==0)
                 cqi(a,b) = 0;
             elseif (tabla_itbs((i-1),2)<sinr(a,b)&& sinr(a,b)<tabla_itbs(i,2))
             cqi(a,b)=tabla_itbs((i-1),1);
             end
             end
       end
end