function [ fi ] = comandosPCAcum(so,srx)
%De acuerdo a la diferencia de la SINR recibida y la SINR objetivo se
%selecciona el valor de fi entre los rangos de [-1 0 1 3]
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
global nues
global nc
fi=zeros(3*nues,nc);
%deltapusch=[-1 1 3];
for i=1:nc
    for j=1:3*nues       
        if ((so+2)>srx(j,i) && srx(j,i)>=so||srx(j,i)==0)
            fi(j,i)=0;
        elseif ((so+4.5)>srx(j,i) && srx(j,i)>(so+2)) 
            fi(j,i)=-1;
        elseif((so-4)<srx(j,i) && srx(j,i)<so)
            fi(j,i)=1; 
        elseif(srx(j,i)<(so-4))
            fi(j,i)=4;
        end
    end
end
end
