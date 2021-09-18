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

function[posx3 posy3]=sector3(ex3,ey3,nue,rd,at,n)

xv3=ex3+(rd*[4/4;4/4;2/4;0;1/4;4/4]);
yv3=ey3+(at*[1;2;2;1;1/2;1]);

%Vectores de posición de UE
posx3=zeros(1,nue);
posy3=zeros(1,nue);
posz3=zeros(1,nue);

%Identificador UE
id=n;

%Creación de UE aleatorios
for k=1:nue
    posx3(k) = ex3 + rd*rand(1);
    posy3(k) = ey3 + at/2 + rand(1)*2*at;
    posz3(k) = 1.5;
    id = id+1;
    in = inpolygon(posx3(k),posy3(k),xv3,yv3);
    while in == false
    posx3(k) = ex3 + rd*rand(1);
    posy3(k) = ey3 + at/2 + rand(1)*2*at;
    in = inpolygon(posx3(k),posy3(k),xv3,yv3);
    end
    hold on;% mantener gráfica
    axis equal; % ejes iguales
    text(posx3(k),posy3(k),posz3(k)+1,['UE ' int2str(id)]);
end
in = inpolygon(posx3,posy3,xv3,yv3);
plot3(posx3(in),posy3(in),posz3(in),'.r');
fill(xv3,yv3,[1 0.1 0.6], 'linewidth',1.2)