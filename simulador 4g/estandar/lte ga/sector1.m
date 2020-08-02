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

function[posx1, posy1,nu]=sector1(ex1,ey1,nue,rd,at)

xv1=ex1+(rd*[1/4;2/4;6/4;7/4;4/4;1/4]);
yv1=ey1+(at*[1/2;0;0;1/2;1;1/2]);

%Vectores de Posición de UE
posx1=zeros(1,nue);
posy1=zeros(1,nue);
posz1=zeros(1,nue);

%Identificador del UE
nu=0;

%Creacion de UE aleatorios
for k=1:nue
    posx1(k) = ex1 + rd/4 + (7*(rd/4))*rand(1);
    posy1(k) = ey1 + rand(1)*at;
    posz1(k) = 1.5;
    nu= nu+1;
    in = inpolygon(posx1(k),posy1(k),xv1,yv1);
    
        while in == false
            posx1(k) = ex1 + rd/4 + (7*(rd/4))*rand(1);
            posy1(k) = ey1 + rand(1)*at;
            in = inpolygon(posx1(k),posy1(k),xv1,yv1);
        end
        hold on; % mantener gráfica
        axis equal; % ejes iguales
        text (posx1(nu),posy1(nu),posz1(nu)+1,['UE' int2str(nu)]);
end
in = inpolygon(posx1,posy1,xv1,yv1);
plot3(posx1(in),posy1(in),posz1(in),'.r')%Puntos dentro del poligono
fill(xv1,yv1,[0.4 0.9 0.2], 'linewidth',1.2);