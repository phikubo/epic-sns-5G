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

function[theta]=theta_ue(pos_uey,posc_bsy,pos_uex,posc_bsx)

        if((pos_uex-posc_bsx)>0 && (pos_uey-posc_bsy>=0))
            theta= atand((pos_uey-posc_bsy)/(pos_uex-posc_bsx));
            
        elseif((pos_uex-posc_bsx)<0)
            theta=atand((pos_uey-posc_bsy)/(pos_uex-posc_bsx))+180;
          
        elseif((pos_uex-posc_bsx)>0 &&(pos_uey-posc_bsy)<0)
            theta= atand((pos_uey-posc_bsy)/(pos_uex-posc_bsx))+360;
        end
end