function [ Ptrans, comando ] = calculoPTRXCL( servicio,serviciocl,ptxol,ptxPL,ptxcl,tpc,iteracion,com,p,so,srx)
%Calculo de la Potencia de transmision de UE en lazo abierto
%Mirar Si tiene servicio o no
%Si tiene servicio calcular lazo cerrado 
%Si no tiene servicio la potencia de transmision es la de lazo abierto
%Autor: Angela Julieth Moreno Delgado
global nues
global nc
Ptrans = zeros(3*nues,nc);
%matrix para guardar los comandos 
comando = zeros(3*nues,nc);

%Calculo de comandos TPC deacuerdo al modo 
switch tpc
    case 1 %Modo Acumulativo
        comando = comandosPCAcum(so,srx); %Comandos Modo Acumulativo
         c = comando + com(iteracion-1).com;
    case 2 %Modo Absoluto
        comando = comandosPCAbs(so,srx); %Comandos Modo Absoluto 
         c = comando;
end
      
for i=1:3*nues
    for j=1:nc
        if(servicio(i,j)==1)
            if(iteracion==2)
            Ptrans(i,j) = ptxPL(i,j) + p(i,j) + c(i,j); %Potencia de transmision calculada con lazo cerrado
            else 
                if(ptxcl(i,j)>=23 && serviciocl(i,j)==0 && c(i,j)>0) % se evalua si se alcanzo anteriormente la potencia max 23dbm y no se tuvo servicio
                    Ptrans(i,j)=0;
                else
                Ptrans(i,j) = ptxcl(i,j) + c(i,j); %Potencia de transmision calculada con lazo cerrado para las iteraciones siguientes
                end
            end
        else
            Ptrans(i,j)= ptxol(i,j); % Si no tiene servicio la potencia es calculada en lazo abierto
        end
        %Validacion de Potencia Maxima
        if (Ptrans(i,j)> 23)
            Ptrans(i,j)=23;
        elseif(Ptrans(i,j)<-43)
            Ptrans(i,j)=-43;
        end
        
    end
end     
end

