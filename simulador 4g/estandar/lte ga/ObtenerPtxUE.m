function [ PtxOL,PmaxOL,PtxOLPL] = ObtenerPtxUE( prb, po, alfa, perdidas,paso)
%Se calcula la potencia de transmision del UE y se valida
%si el resultado obtenido se encuentra entre -43dBnm y 23dBm
global nc
global nues
PtxOL = zeros(3*nues,nc);
PtxOLPL=zeros(3*nues,nc);
PmaxOL = zeros(3*nues,nc);
for i=1:3*nues
    for j=1:nc
        if(prb(i,j)==0)
            PtxOL(i,j)=0;
        else
            PtxOL(i,j)= 10*log10(prb(i,j)) + po + alfa*perdidas(i,j) + paso(i,j);
            PtxOLPL(i,j)= 10*log10(prb(i,j)) + po + alfa*perdidas(i,j);
            if (PtxOL(i,j)> 23)
            PtxOL(i,j)=23;
            PmaxOL(i,j)=1;
        elseif(PtxOL(i,j)<-43)
            PtxOL(i,j)=-43;
            end
        end
    end
end
end