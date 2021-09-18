function dibujoCeldas(axes)
%realiza la gráfica de cobertura teniendo en cuenta el valor de buttonPC,
%que indica si se grafica los resultados de cobertura del algoritmo de
%control de potencia en lazo cerrado o lazo abierto.
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
global UEx
global UEy
global RadiosCobertura
global RadiosCoberturacl
global buttonPC
global seup
global seupcl
global radio
global nc
%Datos
rd = radio;
at=0.866*rd;
Nuser=length(UEx);
t=0:0.1:2.01*pi;

% Valores de ejes de la Celdas
ex = [0 0 6*rd/4 6*rd/4]';
ey = [0 2*at at 3*at]';
f1 = [0 0 0 0 0 0 ];
%Valores de los eNB
x=[1 2.5];
y=[0.866 1.732 2.598 3.464];
XBS=rd*[x(1) x(1) x(2) x(2)];
YBS=rd*[y(1) y(3) y(2) y(4)];

%para optimización
Datos = struct('x1',f1,'y1',f1,'x2',f1,'y2',f1,'x3',f1,'y3',f1);

if (buttonPC == 1)
RdCeldas = RadiosCobertura;
serviup=seup;
else
RdCeldas = RadiosCoberturacl;
serviup=seupcl;
end
for i=1:nc
%Sector1
Datos(i).x1 = ex(i)+(rd*[1/4;2/4;6/4;7/4;4/4;1/4]);
Datos(i).y1 = ey(i)+(at*[1/2;0;0;1/2;1;1/2]);

%Sector2
Datos(i).x2 =ex(i)+(rd*[7/4;8/4;6/4;4/4;4/4;7/4]);
Datos(i).y2=ey(i)+(at*[1/2;1;2;2;1;1/2]);

%Sector3
Datos(i).x3=ex(i)+(rd.*[4/4;4/4;2/4;0;1/4;4/4]);
Datos(i).y3=ey(i)+(at.*[1;2;2;1;1/2;1]);
end

hold (axes,'on');
for i = 1:nc
fill(Datos(i).x1,Datos(i).y1,[0.4 0.9 0.2], 'linewidth',1.2);
%hold on
fill(Datos(i).x2,Datos(i).y2,[0.1 0.7 1], 'linewidth',1.2);
%hold on
fill(Datos(i).x3,Datos(i).y3,[1 0.1 0.6], 'linewidth',1.2)
%hold on
    plot (XBS(i),YBS(i),'^r','MarkerFaceColor','y', 'MarkerSize',6)
%hold on 
end
for i=1:nc
    for j=1:Nuser
        if serviup(j,i) == 1 %Tiene Servicio
            color = [ 0 255 0]/255; % cuando tiene cobertura
            colorRelleno = [ 0 255 0]/255; % cuando tiene cobertura
        else
            color = [ 0 0 0]; 
            colorRelleno = [ 0 0 0]/255; 
        end
        plot(axes,UEx(j,i), UEy(j,i), 'mo', 'color', color, 'linewidth', 2, 'MarkerFaceColor', colorRelleno, 'MarkerSize', 7);
        text (UEx(j,i),UEy(j,i),['UE' int2str(j)]);
    end  
end
%hold on
for i=1:nc
    xx = RdCeldas(1,i)*cos(t) + XBS(i);
    yy = RdCeldas(1,i)*sin(t) + YBS(i);
    plot(xx, yy, 'Color', [0 0 1], 'linewidth', 2);
   % hold on
end
axis([0 3.5*rd 0 4.5*rd]);
hold(axes,'off');
end


