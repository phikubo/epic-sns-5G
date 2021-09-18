function [ intCelda ] = intCeltotal( Celdaint1,Celdaint2,Celdaint3,userc)
%Se crea una estructura en donde para cada UE se guarda las potencias
%interferentes a este en todo el sistema 
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
x=zeros(userc,3);
intCelda =struct('ue',x);
    for j=1:userc
        intCelda(j).ue = [Celdaint1(:,j) Celdaint2(:,j) Celdaint3(:,j)];
    end  
end

