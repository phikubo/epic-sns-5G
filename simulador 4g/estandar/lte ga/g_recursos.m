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

% Simulador Básico a Nivel de Sistema para LTE con Planificadores de Recursos Radio Integrados y Técnicas de Reúso de Frecuencia.
% Licencia academica, no comercial.
% Autor: María Manuela Silva Zambrano, Valentina Giselle Moreno Parra
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2015

%%

function g_recursos(rec,n,prb,rept)

c=[1 0.3 0.5 0 0.2 0.8 1 0.1 0.7 0.4 1 0.3 0.5 1 0.5 0.8 0.7 0.9 0.2 0.4 1 0.5 0.8 0.6 0.5 0.4 0.8 1 1 0.2 0.8 0.4 0.8 0.4 0.4 0.1 0.6 0.8 0.9 0.5 1 0.2 0.8 1 0.9 0.5 0.7 0.3 0.6 0.5;
   1 0.6 0.3 0.9 0.2 1 0.3 0.7 0.3 1 0.2 0.3 0.8 0.4 0.5 0.6 1 0.2 0.9 0.1 0.5 0.7 0.8 0.5 0.4 0.3 0.6 0.3 0.8 0.2 0.4 0 1 0.7 0.8 0.8 0.9 0.3 0.2 0.4 0.5 0.1 0.4 0.7 0.9 0.3 0.6 0.3 0.2 0.5;
   0 1 0 0 0.2 1 0.2 0.7 0.5 0.8 0.8 0.9 0.6 1 0.4 0.5 0.1 0.4 0.7 0.9 0.3 0.6 0.3 0.2 0.5 0.5 1 0.5 0.8 0.7 0.9 0.2 0.4 1 0.5 0.8 0.6 0.5 0.9 0.4 0.3 0.8 0.4 0.1 0.6 0.8 0.9 0.3 0.2 1];

col=[c flipud(c)];

%% para crear leyenda en la que se visualiza número del UE con su respectivo color
c=cellstr(int2str(zeros(1,9)));
t=n+1;

for i=1:n
x=([0;1;1;0;0]); %para empezar desde cero
y=((i-1)+[0;0;1;1;0]);
hold on  
if((t-i)>=1)
fill(x,y,[col(1,t-i) col(2,t-i) col(3,t-i)],'linewidth',1.3)
end
end

for x=1:n
c(x)={['UE ' int2str(t-x)]};
end
legend(cellstr(c))

%%

for a=1:rept % para llenar subtramas(eje X)(columnas de la matriz)
var=0;
prb=0;  
for i=1:n % para recorrer filas de rec (RB asignados por fila(# de ussuarios))
prb=prb+rec(i,a);    
for j=var:prb-1 % para llenar los RB asignados a cada usuario (eje Y)

x=((a-1)+[0;1;1;0;0]); %para empezar desde cero
y=(j+[0;0;1;1;0]);

hold on;
fill(x,y,[col(1,i) col(2,i) col(3,i)],'linewidth',1.6)

end
var=prb;
end
end


%grid on;

set(gcf, 'color', [1 1 1]);
axis([0 rept+3 0 prb+2]);
xlabel('Subtrama');
ylabel('Bloques de recursos');

