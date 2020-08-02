function[prb_PFup]=plan_Proportional_FairUP(ser,tbs,SINRu,tp_PF)
%Asignacion de Recursos para el UL utilizando el planificador Proportional
%Fair
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
global nc;
global nues;
global prb;
userc =3*nues;
tabla_capacidad= xlsread('capacidad.xls');

p=zeros(1,nc);
tmu=zeros(userc,nc);
prb_PFup=zeros(userc,nc);

UeActi=sum(ser); %suma los UE que tienen servicio en cada celda generando un vector de 1x4columnas

for i=1:userc 
     for j=1:nc
         if (ser(i,j)==0)
             tmu(i,j)=0;
         else
          tmu(i,j)=tabla_capacidad(tbs(i,j)+2,prb+1);   %throuhput maxima a partir del tbs y 15 prb
         end
          p(i,j)=tmu(i,j)/(tp_PF(:,j)); % prioridad de asignación de cada usuario 
     end
end
ptj=sum(p); %suma de prioridades
for i=1:nc
    for j=1:userc    
        prb_PFup(j,i)= p(j,i)/(ptj(1,i)); %división de prioridad entre suma d eprioridades
    end
end
%Asignación de 1RB a los UE activos en cada Celda
%se hace 4 veces porque no sabemos los UE activos en cada celda
prba1 = prb - UeActi(1); %Asignaciíon de un prb a cada UEctivo en la celda 1, prba1 = Número de prbs a asignar realmente en la c4lda1
prba2 = prb - UeActi(2);
prba3 = prb - UeActi(3);
prba4 = prb - UeActi(4);
%--------------------------------------------------------------
prb_PFup(:,1) = floor(prb_PFup(:,1).*prba1)+1;
prb_PFup(:,2) = floor(prb_PFup(:,2).*prba2)+1;
prb_PFup(:,3) = floor(prb_PFup(:,3).*prba3)+1;
prb_PFup(:,4) = floor(prb_PFup(:,4).*prba4)+1;
for i=1:userc
    for j=1:nc
        if(ser(i,j)==0)
            prb_PFup(i,j)=0;
        end
    end
end
 
R1=sort((SINRu),'descend'); %Organizar la SINR en orden de mayor a menor

prun=prb-sum(prb_PFup); %vector [#RBcelda1 #RBcelda2 #RBcelda3 #RBcelda4] Matrix 1x4 de prb que estan disponibles para asignar en cada celda
%Falta asignar los recursos que quedan prun en los UE activos
for c=1:nc
    for i=1:UeActi(c)    
        for j=1:userc
            if(R1(i,c)==SINRu(j,c) && ser(j,c)==1)
                if(prun(1,c)>0)  
                    prb_PFup(j,c)= prb_PFup(j,c)+1;
                    prun(1,c)=prun(1,c)-1;
                end  
            end       
        end  
    end
end

