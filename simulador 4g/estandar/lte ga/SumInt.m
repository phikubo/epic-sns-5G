function [ sumCelda ] = SumInt(p1,p2,p3,p4,userc)
%Se obtiene la PRX interferente para cada uno de los UE del sistema LTE.
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
x=zeros(1,userc);
    eNB1sin= x;
    eNB1lento= x;
    eNB1rapido= x;
    
    eNB2sin = x;
    eNB2lento= x;
    eNB2rapido= x;
    
    eNB3sin = x;
    eNB3lento= x;
    eNB3rapido= x;
    
    eNB4sin = x;
    eNB4lento= x;
    eNB4rapido= x;

for i=1:userc
    eNB1sin(i) = sum(sum(p1.sin(i).ue));%-cuen(i,1);
    eNB1lento(i)=sum(sum(p1.lento(i).ue));%-cuen(i,1);
    eNB1rapido(i)=sum(sum(p1.rapido(i).ue));%-cuen(i,1);
    
    eNB2sin(i) = sum(sum(p2.sin(i).ue));%-cuen(i,2);
    eNB2lento(i)=sum(sum(p2.lento(i).ue));%-cuen(i,2);
    eNB2rapido(i)=sum(sum(p2.rapido(i).ue));%-cuen(i,2);
    
    eNB3sin(i) = sum(sum(p3.sin(i).ue));%-cuen(i,3);
    eNB3lento(i)=sum(sum(p3.lento(i).ue));%-cuen(i,3);
    eNB3rapido(i)=sum(sum(p3.rapido(i).ue));%-cuen(i,3);
    
    eNB4sin(i) = sum(sum(p4.sin(i).ue));%-cuen(i,4);
    eNB4lento(i)=sum(sum(p4.lento(i).ue));%-cuen(i,4);
    eNB4rapido(i)=sum(sum(p4.rapido(i).ue));%-cuen(i,4);

end
sumCelda.sin =[eNB1sin' eNB2sin' eNB3sin' eNB4sin'];
sumCelda.lento =[eNB1lento' eNB2lento' eNB3lento' eNB4lento'];
sumCelda.rapido=[eNB1rapido' eNB2rapido' eNB3rapido' eNB4rapido'];
end

