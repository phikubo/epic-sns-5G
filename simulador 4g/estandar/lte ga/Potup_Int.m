function[PotenciaI]=Potup_Int(nc,userc, Lup, Ptxue, IntCel)
% CALCULO DE LA POTENCIA DE Rx Interferente.
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
GeNB = 18;
mp=nc-1;
prx_i =zeros(userc,mp);
%---------------------------------
x=zeros(userc,nc);
PotenciaI =struct('ue',x);
%---------------------------------
for i=1:userc
    UEi=IntCel(i).ue; %Matriz de Interferencia a la señal del UEi de la celda de estudio
    prxcero =ones(userc,mp); %Matriz que identifica cuando la potencia recibida es cero
    for j=1:mp
        for k=1:userc
        if UEi(k,j)== 1  %Si el UEk del eNBj es interferente a la celda de estudio
            if(Ptxue(k,j)==0) %Si la potencia del UE interferente es cero
                prx_i(k,j)=0;
                prxcero(k,j)=0;
            else
                prx_i(k,j)= Ptxue(k,j)+ GeNB -Lup(k,j); 
                prxcero(k,j)=1;%por asegurarse
            end
        else
            prx_i(k,j)=0;
            prxcero(k,j)=0;
        end
        end
    end
    PotenciaI.sin(i).ue= 10.^(prx_i/10).*prxcero;
    M1= randn(userc,mp);
    prx_int_des_l= (M1 + prx_i); %Desvanecimiento Lento
    pdl_iv=10.^( prx_int_des_l/10);
    PotenciaI.lento(i).ue=pdl_iv.*prxcero;
    
    rel_vol_int= sqrt(pdl_iv);
    b_int= rel_vol_int/sqrt(pi./2);
    vol_int_des_rl_v= raylrnd(b_int);  % desvanecimiento rapido
    pdr_iv=((vol_int_des_rl_v).^2);
    PotenciaI.rapido(i).ue=pdr_iv.*prxcero;
end
end








