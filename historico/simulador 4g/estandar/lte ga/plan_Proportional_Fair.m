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

function[prb_PF]=plan_Proportional_Fair(mi,tp_PF,tbs,SINR,prb,nue)

% tp_PF=[1500 1200 1500 1200];
% 
% tbs=[26 2 0 0;
%     7 7 2 0;
%     9 13 2 9;
%     9 2 9 13;
%     0 5 13 18;
%     2 18 13 15];
% 
% SINR=[23.8321 -2.2998 -4.8743 -6.5043;
%       2.7535 3.6701 -1.6796 -17.3179;
%       5.2182 8.8422 -1.1481 4.3259;
%       4.5459 -1.4312 5.6626 10.1497;
%       -10.5456 1.5420 8.8411 12.8808;
%       0.0719 13.9950 8.1162 11.0557];
% 
% prb=25;
% nue=6;

p=zeros(1,mi);
tmu=zeros(nue,mi);
prb_PF=zeros(nue,mi);

tabla_capacidad= xlsread('capacidad.xls');

for i=1:nue 
     for j=1:mi
       tmu(i,j)=tabla_capacidad(tbs(i,j)+2,prb+1);   %throuhput maxima a partir del tbs y 15 prb
     end
end


for i=1:mi
    for j=1:nue     
        p(j,i)=tmu(j,i)/(tp_PF(:,i)); % prioridad de asignación de cada usuario
    end
end

ptj=sum(p); %suma de prioridades

for i=1:mi
    for j=1:nue    
        prb_PF(j,i)=p(j,i)/(ptj(1,i)); %división de prioridad entre suma d eprioridades
    end
end

prba=prb-(nue);% asignación de un prb a cada usuario, prba=número de prbs a asignar realmente
prb_PF=floor(prb_PF*prba)+1;
prun=prb-sum(prb_PF);

R1=sort((SINR),'descend');

for c=1:mi
    for i=1:nue    
        for j=1:nue
            if(R1(i,c)==SINR(j,c))
                if(prun(1,c)>0)  
                    prb_PF(j,c)= prb_PF(j,c)+1;
                    prun(1,c)=prun(1,c)-1;
                end  
            end       
        end  
    end
end

