function [ sub ] = subportadora(sche,users)
%Variable que indica que conjunto de subportadora posee el UE de la celda
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
userc=3*users;
n=1;
x=zeros(1,userc);
sub =struct('ue',x);
for i=1:userc
    subpor = zeros(1,sche(i)); %Para mayor rapidez
    for j=1:sche(i)
    subpor(j)=n;
    n=n+1;
    end
    sub(i).ue = subpor;
end

