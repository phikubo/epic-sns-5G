function [ ServiUE, UEsi,UEno, dis ] = servicio( SinrTarget,sinr,dist,ptx )
%Esta funcion retrona la matriz de 1 y 0 para indicar que UE tienen
%servicio en el sistema, el numero de UE con y sin servicio y las
%distancias de los UE con servicio en cada celda. 
%para ello se pide la sinr objetivo, sinr recibida en el eNB y las
%distancias de todos los UEs.
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
global nc
global nues
UEsi=0; %Numero de UE con servicio
UEno=0; %Numero de UE sin servicio
ServiUE=zeros(3*nues,nc);
dis= zeros(3*nues,nc); %Matriz para guardar las distancias de los UE con servicio
%En el sistema cuando hay una sinr que es exactamente cero el UE no
%trasmitio y de le a dado este valor para identificarlo
for i=1:nc
    for j=1:3*nues
        if ptx(j,i)==0
            ServiUE(j,i) = 0; %el UE no tiene servicio
            dis(j,i)= 0;
            UEno = UEno + 1;
        elseif (sinr(j,i)>SinrTarget)
            UEsi =  UEsi + 1;
            ServiUE(j,i) = 1; %el UE tiene servicio
            dis(j,i)=dist(j,i);
        else
            ServiUE(j,i) = 0; %el UE no tiene servicio
            dis(j,i)= 0;
            UEno = UEno + 1;
        end
    end
end

end

