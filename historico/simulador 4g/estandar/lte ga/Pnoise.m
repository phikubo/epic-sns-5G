function [ potnoise ] = Pnoise( prb )
%Calcula el ruido del sistema para cada uno de los UE del sistema deacuerdo
%al numero de bloques de recursos que se le hayan asignados en el enlace
%descendente
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
global nc
global nues
potnoise=zeros(3*nues,nc);
Pruido=zeros(3*nues,nc);
for i=1:nc
    for j=1:3*nues
        if(prb(j,i)==0)
            potnoise(j,i)=0;
        else
            Pruido(j,i)=10*log10(1.38*10^(-23))+10*log10(290)+10*log10(prb(j,i)*180000) + 30; 
            potnoise(j,i)= 10^(Pruido(j,i)/10);   %potencia de ruido en mW
        end
    end
end      
end

