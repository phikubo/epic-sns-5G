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

function[prb_MR]=plan_Maximun_Rate(mi,vm,tbs,SINR,prb,nue)

% tp_PF=[1500 1200 1500 1200];
% tbs=[ 2 2 11 5;
%       4 9  7 0;
%       3 2 13 5;
%       2 7  7 7;
%       4 5 7 11;
%       0 9 9 7;
%       0 7 11 11; 
%       4 13 13 7;
%       0 11 7 7];
%     
% prb=15;
% nue=9;
% vm=10;

p=zeros(1,mi);
tmu=zeros(nue,mi);
prb_MR=zeros(nue,mi);

tabla_capacidad= xlsread('capacidad.xls');

for j=1:mi
    
  min=vm; %%UE con Tbs menor o igual a min. no son considerados para asiganar recursos
    
    for i=1:nue 
        
         if(tbs(i,j)<=min)
              tmu(i,j)=0;
         else
              tmu(i,j)=tabla_capacidad(tbs(i,j)+2,prb+1);   %throuhput maxima a partir del tbs y #max. de prb
         end
     end
         
    while(sum(tmu(:,j))==0)%%en caso de que todos los usuarios tengan unas condiciones de canal malas se elige "el  mejor de los peores"
        
        min=min-1;
        
        for i=1:nue 
        if(tbs(i,j)<=min)
              tmu(i,j)=0;
        else
              tmu(i,j)=tabla_capacidad(tbs(i,j)+2,prb+1);   %throuhput maxima a partir del tbs y #max. de prb
        end
        end
            
    end
         
end

for i=1:mi
    for j=1:nue 
        
p(j,i)=tmu(j,i)/1; % prioridad de asignación de cada usuario
    end
end

ptj=sum(p); %suma de prioridades

for i=1:mi
    for j=1:nue 
        
prb_MR(j,i)=p(j,i)/(ptj(1,i)); %división de prioridad entre suma de prioridades
    end
end

prb_MR=floor(prb_MR*prb);
prun=prb-sum(prb_MR);

R1=sort((SINR),'descend');

for c=1:mi
for i=1:nue    
    for j=1:nue
   
      if(R1(i,c)==SINR(j,c))
      if(prun(1,c)>0)  
      
       prb_MR(j,c)= prb_MR(j,c)+1;
       prun(1,c)=prun(1,c)-1;
       
      end  
       end
            
    end  
end
end

