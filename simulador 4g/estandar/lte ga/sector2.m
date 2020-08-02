% Simulador Básico a Nivel de Sistema para LTE.
% Licencia academica, no comercial.
% Autor: Claudia Shirley Paz Arteaga, Eileen Johana Martinez Gómez
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2014

% Simulador Básico a Nivel de Sistema para LTE con Planificadores de Recursos Radio Integrados.
% Licencia academica, no comercial.
% Autor: Darío Giraldo Medina, Diego Fernando Uribe Ante
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2015

%%

function[posx2 posy2 n]=sector2(ex2,ey2,nue,rd,at,n1)

xv2=ex2+(rd*[7/4;8/4;6/4;4/4;4/4;7/4]);
yv2=ey2+(at*[1/2;1;2;2;1;1/2]);

%Vectores de posición de UE
posx2=zeros(1,nue);
posy2=zeros(1,nue);
posz2=zeros(1,nue);

%identificador UE en la celda
n=n1;
%Creacion de UE aleatorios
for k=1:nue
    posx2(k) = ex2 + rd + (8*(rd/4))*rand(1);
    posy2(k) = ey2 + at/2 + rand(1)*2*at;
    posz2(k) = 1.5;
    n = n+1;
    in = inpolygon(posx2(k),posy2(k),xv2,yv2);
    while in == false
    posx2(k) = ex2 + rd + (8*(rd/4))*rand(1);
    posy2(k) = ey2 + at/2 + rand(1)*2*at;
    in = inpolygon(posx2(k),posy2(k),xv2,yv2);
    end
    hold on; % mantener gráfica
    axis equal; % ejes iguales
    text(posx2(k),posy2(k),posz2(k)+1,['UE ' int2str(n)]);
end
in = inpolygon(posx2,posy2,xv2,yv2);
plot3(posx2(in),posy2(in),posz2(in),'.r');
fill(xv2,yv2,[0.1 0.7 1], 'linewidth',1.2);