function [ inter ] = InterfeUp( Celda , Celdaint, userc )
%Identifica que UEs de la Celda interferente (Celdaint) interfieren con los
%UE de la celda de estudio (Celda).
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016

UEint = zeros(userc,userc);

for i =1: userc
    v = Celda(i).ue;
    for j=1:userc
        u = Celdaint(j).ue;
        w=zeros(1,length(u));
        for k=1:length(u) %Se revisa que subportadoras se tienen en comun
            if find(v == u(k))>=1 %si algun subconjunto de portadoras de u se encuentra en v
                w(k)=1; %Tiene portadora en comun
            else
                w(k)=0;
            end
        end
        x =sum(w);
            if x >= 1 
                UEint(j,i)=1; %indico el UE interfiere de Celaint al UE de Celda de estudio (Celda)
            else
                UEint(j,i)=0;
            end
    end
end  
inter = UEint;
end

