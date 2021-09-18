% Simulador B�sico a Nivel de Sistema para LTE.
% Licencia academica, no comercial.
% Autor: Claudia Shirley Paz Arteaga, Eileen Johana Martinez G�mez
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2014

% Simulador B�sico a Nivel de Sistema para LTE con Planificadores de Recursos Radio Integrados.
% Licencia academica, no comercial.
% Autor: Dar�o Giraldo Medina, Diego Fernando Uribe Ante
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2015

% Simulador B�sico a Nivel de Sistema para LTE con Planificadores de Recursos Radio Integrados y T�cnicas de Re�so de Frecuencia.
% Licencia academica, no comercial.
% Autor: Mar�a Manuela Silva Zambrano, Valentina Giselle Moreno Parra
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2015

% Simulador B�sico a Nivel de Sistema para LTE con Algoritmos de Control de Potencia.
% Licencia academica, no comercial.
% Autor: Angela Julieth Moreno Delgado.
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2016

%%
% Definici�n del escenario
clear all;
clc;
valores=dlmread('valores.dat');

%cuando los vectores tp_RR y tp_PF sse llenen de ceros se deben descomentar
%estas lineas, el
% ssss=[1500 1200 1500 1200];
% dlmwrite('RP_RR.dat', ssss, 'delimiter', '\n', 'precision', '%.4f','-append');
% dlmwrite('RP_PF.dat', ssss, 'delimiter', '\n', 'precision', '%.4f','-append');
% kkkkk

tp_RR=(dlmread('RP_RR.dat')'); 
tp_PF=(dlmread('RP_PF.dat')');
tp_PFup=(dlmread('RP_PF.dat')');

global ta
global desvanecimiento
global modelo
global nues
global fr
global po
global BW
global radio
global hant
global planificador
global minMR
%
global estudio
global RR1 RR2 RR3 RR4
global PF1 PF2 PF3 PF4
global PF1up PF2up PF3up PF4up
global PF1upcl PF2upcl PF3upcl PF4upcl
global MR1 MR2 MR3 MR4

global minSINR
global prb rept NumSim

global throughput_c1_RR throughput_c2_RR throughput_c3_RR throughput_c4_RR
global throughput_c1_PF throughput_c2_PF throughput_c3_PF throughput_c4_PF
global throughput_c1_MR throughput_c2_MR throughput_c3_MR throughput_c4_MR
global throughput_c1_PFup throughput_c2_PFup throughput_c3_PFup throughput_c4_PFup
global throughput_c1_PFupcl throughput_c2_PFupcl throughput_c3_PFupcl throughput_c4_PFupcl
global SINR_c1 SINR_c2 SINR_c3 SINR_c4 SINR_T
global SINRup_c1 SINRup_c2 SINRup_c3 SINRup_c4 
global SINRupcl_c1 SINRupcl_c2 SINRupcl_c3 SINRupcl_c4 
global PRX1 PRX2 PRX3 PRX4
global PRXup1 PRXup2 PRXup3 PRXup4
global PRXup1cl PRXup2cl PRXup3cl PRXup4cl
global Radio1 Radio2 Radio3 Radio4
global Radio1cl Radio2cl Radio3cl Radio4cl
global Prob
global Probcl
global Interferencia

global nc
global RadiosCobertura
global RadiosCoberturacl
global UEx
global UEy
global seup
global seupcl
global contador
global nombre_secuencia_tbs
global nombre_secuencia_snr
%% Valores asignados desde la GUI
contador=0
nombre_secuencia_tbs='tbs';
nombre_secuencia_snr='snr';
nombre_secuencia_prb='prbs'
ta=valores(1);
desvanecimiento=valores(2);
modelo=valores(3);
nues=valores(4);
fr=valores(5);
po=valores(6);
BW=valores(7);
radio=valores(8);
planificador=3;
minMR=valores(10); % CQI maximo 14 || >SINR objetivo 4.4dB

NumSim=0;
hant=30;
estudio=2;

nc=4;

%Valores para Algoritmo de PC
load ValoresPC.mat alphapc sinrpc coberpc TPC iterpc;
%N�mero de iteraciones
rept= iterpc;
%Factor de Compensaci�n
alpha = alphapc;
%SNR objetivo en Lazo Abierto
SNRo = sinrpc;
%Cobertura para graficas
pp = 100/coberpc;
CoberUE = ceil(rept/pp);
%Comando de control de Potencia
comTPC = TPC;
%Potencia Max UE
PcmaxUE = 23; %dbm
%Ganancia de antena de eNB
GeNB = 18; % dbi

tra1=zeros(1,rept);
tra2=zeros(1,rept);
tra3=zeros(1,rept);
tra4=zeros(1,rept);

Probabilidad=zeros(1,rept);
Probabilidadcl=zeros(1,rept);
%------------------------------
%% Creacion de matrices llenas de ceros (para optimizaci�n del c�digo)

SINR_c1=zeros((nues*3),rept);
SINR_c2=zeros((nues*3),rept);
SINR_c3=zeros((nues*3),rept);
SINR_c4=zeros((nues*3),rept);
SINR_T =zeros(((nues*3)*rept),4);
SINR=zeros((nues*3),4);

PRX1=zeros((nues*3),rept);
PRX2=zeros((nues*3),rept);
PRX3=zeros((nues*3),rept);
PRX4=zeros((nues*3),rept);

PRXup1=zeros((nues*3),rept);
PRXup2=zeros((nues*3),rept);
PRXup3=zeros((nues*3),rept);
PRXup4=zeros((nues*3),rept);

throughput_c1_RR=zeros((nues*3), rept);
throughput_c1_PF=zeros((nues*3), rept);
throughput_c1_MR=zeros((nues*3), rept);

throughput_c2_RR=zeros((nues*3), rept);
throughput_c2_PF=zeros((nues*3), rept);
throughput_c2_MR=zeros((nues*3), rept);

throughput_c3_RR=zeros((nues*3), rept);
throughput_c3_PF=zeros((nues*3), rept);
throughput_c3_MR=zeros((nues*3), rept);

throughput_c4_RR=zeros((nues*3), rept);
throughput_c4_PF=zeros((nues*3), rept);
throughput_c4_MR=zeros((nues*3), rept);

throughput_RR=zeros((nues*3),4);
throughput_PF=zeros((nues*3),4);
throughput_MR=zeros((nues*3),4);

potmw=po*1000;
ap=0.866*radio;


%% Sectorizaci�n del sistema y posicion de los UE
dist_ue_bs1=zeros((nues*3),4);
dist_ue_bs2=zeros((nues*3),4);
dist_ue_bs3=zeros((nues*3),4);
dist_ue_bs4=zeros((nues*3),4);

dist_bs1=zeros((nues*3),4);
dist_bs2=zeros((nues*3),4);
dist_bs3=zeros((nues*3),4);
dist_bs4=zeros((nues*3),4);

thetac1=zeros((nues*3),4);
thetac2=zeros((nues*3),4);
thetac3=zeros((nues*3),4);
thetac4=zeros((nues*3),4);
%--------------------------------------------------------------------
%figure
%celda 1
%[posx, posy,n]=sector1(0,0,nues,radio,ap);
%pos1=[posx;posy]';
%[posx, posy,n]=sector2(0,0,nues,radio,ap,n);
%pos2=[posx;posy]';

%[posx, posy]=sector3(0,0,nues,radio,ap,n);
%pos3=[posx;posy]';

%pos_ue_celda1=[pos1;pos2;pos3];

%-------------------------------------------------------------
%celda 2
%[posx, posy,n]=sector1(0,2*ap,nues,radio,ap);
%pos1=[posx;posy]';

%[posx, posy,n]=sector2(0,2*ap,nues,radio,ap,n);
%pos2=[posx;posy]';

%[posx, posy]=sector3(0,2*ap,nues,radio,ap,n);
%pos3=[posx;posy]';

%pos_ue_celda2=[pos1;pos2;pos3];

%-------------------------------------------------------------
%celda 3
%[posx, posy,n]=sector1((6*radio/4),ap,nues,radio,ap);
%pos1=[posx;posy]';

%[posx, posy,n]=sector2((6*radio/4),ap,nues,radio,ap,n);
%pos2=[posx;posy]';

%[posx, posy]=sector3((6*radio/4),ap,nues,radio,ap,n);
%pos3=[posx;posy]';

%pos_ue_celda3=[pos1;pos2;pos3];

%-------------------------------------------------------------
%celda 4
%[posx,posy,n]=sector1((6*radio/4),3*ap,nues,radio,ap);
%pos1=[posx;posy]';

%[posx,posy,n]=sector2((6*radio/4),3*ap,nues,radio,ap,n);
%pos2=[posx;posy]';

%[posx, posy]=sector3((6*radio/4),3*ap,nues,radio,ap,n);
%pos3=[posx;posy]';

%pos_ue_celda4=[pos1;pos2;pos3];

%Posiciones en x de UE
%UEx = [pos_ue_celda1(:,1) pos_ue_celda2(:,1) pos_ue_celda3(:,1) pos_ue_celda4(:,1)];

%Posiciones en y de UE
%UEy = [pos_ue_celda1(:,2) pos_ue_celda2(:,2) pos_ue_celda3(:,2) pos_ue_celda4(:,2)];

%save -ascii ues_cord_x.txt UEx;
%save -ascii ues_cord_y.txt UEy;
%save -ascii cord_ue1.txt pos_ue_celda1;
%save -ascii cord_ue2.txt pos_ue_celda2;
%save -ascii cord_ue3.txt pos_ue_celda3;
%save -ascii cord_ue4.txt pos_ue_celda4;
UEx=load('ues_cord_x.txt');
UEy=load('ues_cord_y.txt');
pos_ue_celda1=load('cord_ue1.txt');
pos_ue_celda2=load('cord_ue2.txt');
pos_ue_celda3=load('cord_ue3.txt');
pos_ue_celda4=load('cord_ue4.txt');
%% Coordenadas de las celdas celulares y ubicaci�n de los eNB

x=[1 2.5];
y=[0.866 1.732 2.598 3.464];

XBS=radio*[x(1) x(1) x(2) x(2)];
YBS=radio*[y(1) y(3) y(2) y(4)];
posc_bs=[XBS;YBS]';

%for i=1:length(XBS)
%    plot3(XBS(i),YBS(i),0:0.1:hant,'.b');
%end

%set(gcf,'color', [1 1 1],'Name','Escenario de estudio','NumberTitle','off');
%axis([-radio/2 4*radio -radio/2 4.8*radio 0 1.5*radio]);
%xlabel('Eje X');
%ylabel('Eje Y');
%zlabel('Eje Z');
%view(3)
%grid on;


%% C�lculo de distancia y �ngulo(theta) entre eNB y UE
for i=1:length(posc_bs)
    for j=1:length(pos_ue_celda1)
        %las distbsx son para realizar la grafica en dos dimensiones
        dist_bs1(j,i)=(sqrt((pos_ue_celda1(j,1)-posc_bs(i,1))^2+(pos_ue_celda1(j,2)-posc_bs(i,2))^2));
        dist_bs2(j,i)=(sqrt((pos_ue_celda2(j,1)-posc_bs(i,1))^2+(pos_ue_celda2(j,2)-posc_bs(i,2))^2));
        dist_bs3(j,i)=(sqrt((pos_ue_celda3(j,1)-posc_bs(i,1))^2+(pos_ue_celda3(j,2)-posc_bs(i,2))^2));
        dist_bs4(j,i)=(sqrt((pos_ue_celda4(j,1)-posc_bs(i,1))^2+(pos_ue_celda4(j,2)-posc_bs(i,2))^2));
        
        dist_ue_bs1(j,i)=(sqrt((pos_ue_celda1(j,1)-posc_bs(i,1))^2+(pos_ue_celda1(j,2)-posc_bs(i,2))^2+((1.5-hant)^2)))/1000;
        dist_ue_bs2(j,i)=(sqrt((pos_ue_celda2(j,1)-posc_bs(i,1))^2+(pos_ue_celda2(j,2)-posc_bs(i,2))^2+((1.5-hant)^2)))/1000;
        dist_ue_bs3(j,i)=(sqrt((pos_ue_celda3(j,1)-posc_bs(i,1))^2+(pos_ue_celda3(j,2)-posc_bs(i,2))^2+((1.5-hant)^2)))/1000;
        dist_ue_bs4(j,i)=(sqrt((pos_ue_celda4(j,1)-posc_bs(i,1))^2+(pos_ue_celda4(j,2)-posc_bs(i,2))^2+((1.5-hant)^2)))/1000;
        
        thetac1(j,i)=theta_ue(pos_ue_celda1(j,2),posc_bs(i,2),pos_ue_celda1(j,1),posc_bs(i,1));
        thetac2(j,i)=theta_ue(pos_ue_celda2(j,2),posc_bs(i,2),pos_ue_celda2(j,1),posc_bs(i,1));
        thetac3(j,i)=theta_ue(pos_ue_celda3(j,2),posc_bs(i,2),pos_ue_celda3(j,1),posc_bs(i,1));
        thetac4(j,i)=theta_ue(pos_ue_celda4(j,2),posc_bs(i,2),pos_ue_celda4(j,1),posc_bs(i,1));                 
   end
end

%% Asignaci�n de recusos
rc=load('recursos.dat');
bw=rc(BW,1)*(10^6);
prb=rc(BW,2);
bw_ue= bw/(3*nues);

%% Asignaci�n de la ganancia de la antena
[Gc1,Gc2,Gc3,Gc4]=ganancia(ta,3*nues,thetac1, thetac2, thetac3, thetac4);
G=[Gc1(:,1),Gc2(:,2),Gc3(:,3),Gc4(:,4)];

%% Calculo de p�rdidas de acuerdo al modelo de propagacion DL.
[Lc1, Lc2, Lc3, Lc4]=perdidas(modelo, 3*nues,dist_ue_bs1, dist_ue_bs2, dist_ue_bs3, dist_ue_bs4, fr);

%% Valores estaticos de PC
%Potencia de Ruido por RB
PRB = 10*log10(1.38*10^(-23)) + 10*log10(290) +10*log10(180000)+ 30; %en dBm
% Potencia que el eNB espera recibir por RB
Po = alpha*(SNRo + PRB) + (1 - alpha)*(PcmaxUE);
%Potencia de Tx eNB
PtxENB = 10*log10(potmw); %dbm

% frecuencia en uplink banda 1,2 y 3
if (fr == 1710)
    fup = 1710; %MHz
elseif (fr == 1900)
    fup = 1850; 
else
    fup = 1920;
end
% Perdidas de propagaci�n en UL de acuerdo al modelo de propagacion.
[Lup1, Lup2, Lup3, Lup4] = perdidas(modelo, 3*nues,dist_ue_bs1, dist_ue_bs2, dist_ue_bs3, dist_ue_bs4, fup);

%Parametro para CLPC
z=zeros(3*nues,nc); %indica el tama�o de la estructura
compc =struct('com',z);
%Parametro para guardar las SINR del CLPC
SINRcl = struct('ue',z);
SINRol = struct('ue',z); %para prueba
%Parametro para guardar las Potencias transmitidas calculadas con OLPC
PTXUEol = struct('ue',z);
%Parametro para guardar si se alcanzo a conectar en la red el UE 
Service = struct('ue',z);
%Parametro para guardar matriz que indica con 1 que el UE transmite con Potencia Maxima
Pmax = struct ('ue',z);
%parametro para guardar potencias ceros donde el cero identifica que el UE no transmite
potenciaol = ones(3*nues,nc);
potenciamax = zeros(3*nues,nc);
%Parametro para guardar pasos ol
Pstep = struct('ue',z);
%parametro para guardar los pasos y la sumatoria de estos en cada iteracion
pasos = zeros(3*nues,nc);
%PArametro para guardar la potencia transmitida en cada iteracion del UE (OLPC y CLPC)
Ptransmision = struct('ue',z);
%Matrix para guardar los pasos donde se alcanza el servicio
savestep =zeros(3*nues,nc);
%Parametro para guardar cuando un UE alcanza el servicio al menos 1 vez
serviciocte=zeros(3*nues,nc);
%Parametro para guardar la matrix de servicio generada en cada iteracion
ServicioCL= struct('ue',z);
tic;
for i=1:3
run ('Cargando')
end

%->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

for NumSim=1:rept
NumSim
%% Calculo de potencias en cada celda

% Celda1
[prx, pdl, pdr]=pot_celda(1, 3*nues, Gc1, Lc1, potmw);
prx1=prx;
prx1_des_l=pdl;
prx1_des_rl=pdr;

% Celda2
[prx, pdl, pdr]=pot_celda(2, 3*nues, Gc2, Lc2, potmw);
prx2=prx;
prx2_des_l=pdl;
prx2_des_rl=pdr;

% Celda3
[prx, pdl, pdr]=pot_celda(3, 3*nues, Gc3, Lc3, potmw);
prx3=prx;
prx3_des_l=pdl;
prx3_des_rl=pdr;

% Celda4
[prx, pdl, pdr]=pot_celda(4, 3*nues, Gc4, Lc4, potmw);
prx4=prx;
prx4_des_l=pdl;
prx4_des_rl=pdr;

%% Calculo de potencias interferentes.
%Perdidas de BS de otras celdas hacia los usuarios de la celda1        
    Lci_1=[Lc1(:,2) Lc1(:,3) Lc1(:,4)];
    Gci_1=[Gc1(:,2) Gc1(:,3) Gc1(:,4)];
  
%Perdidas de BS de otras celdas hacia los usuarios de la celda2       
    Lci_2=[Lc2(:,1) Lc2(:,3) Lc2(:,4)];
    Gci_2=[Gc2(:,1) Gc2(:,3) Gc2(:,4)];
    
%Perdidas de BS de otras celdas hacia los usuarios de la celda3
    Lci_3=[Lc3(:,1) Lc3(:,2) Lc3(:,4)];
    Gci_3=[Gc3(:,1) Gc3(:,2) Gc3(:,4)];
    
%Perdidas de BS de otras celdas hacia los usuarios de la celda4
    Lci_4=[Lc4(:,1) Lc4(:,2) Lc4(:,3)];
    Gci_4=[Gc4(:,1) Gc4(:,2) Gc4(:,3)];
 
%% CALCULO DE LA POTENCIA DE Rx Interferente.

% Celda1
[prx_i, pdl_iv, pdr_iv]=pot_int(nc,3*nues, Gci_1, Lci_1, potmw);
prx_int1=prx_i';
prx_int1_des_lv=pdl_iv';
prx_int1_des_rl_v=pdr_iv';

% Celda2
[prx_i, pdl_iv, pdr_iv]=pot_int(nc,3*nues, Gci_2, Lci_2, potmw);
prx_int2=prx_i';
prx_int2_des_lv=pdl_iv';
prx_int2_des_rl_v=pdr_iv';

% Celda3
[prx_i, pdl_iv, pdr_iv]=pot_int(nc,3*nues, Gci_3, Lci_3, potmw);
prx_int3=prx_i';
prx_int3_des_lv=pdl_iv';
prx_int3_des_rl_v=pdr_iv';

% Celda4
[prx_i, pdl_iv, pdr_iv]=pot_int(nc,3*nues, Gci_4, Lci_4, potmw);
prx_int4=prx_i';
prx_int4_des_lv=pdl_iv';
prx_int4_des_rl_v=pdr_iv';

%% Calculo interferencias totales hacia los UE en la celda "x" por parte de los eNB de otras celdas
switch desvanecimiento
  case 2
  interferencia_c1_v=(sum(prx_int1_des_lv)); 
  interferencia_c2_v=(sum(prx_int2_des_lv));
  interferencia_c3_v=(sum(prx_int3_des_lv));
  interferencia_c4_v=(sum(prx_int4_des_lv));   

  case 3      
  interferencia_c1_v=(sum(prx_int1_des_rl_v)); 
  interferencia_c2_v=(sum(prx_int2_des_rl_v));
  interferencia_c3_v=(sum(prx_int3_des_rl_v));
  interferencia_c4_v=(sum(prx_int4_des_rl_v));
  
  case 4
  prx_int1v=10.^(prx_int1./10);
  prx_int2v=10.^(prx_int2./10);
  prx_int3v=10.^(prx_int3./10);
  prx_int4v=10.^(prx_int4./10);
  interferencia_c1_v=(sum( prx_int1v)); 
  interferencia_c2_v=(sum( prx_int2v));
  interferencia_c3_v=(sum( prx_int3v));
  interferencia_c4_v=(sum( prx_int4v));     
end   
Interferencia= [interferencia_c1_v interferencia_c2_v interferencia_c3_v interferencia_c4_v];

%% C�lculo de Ruido t�rmico en el sistema
pn=(-174.2855251)+10*log10(bw_ue);
pn_v= (10.^(pn./10));   %potencia de ruido en mW

%% Calculo interferencias totales hacia los usuarios de la celda x de las otras BS MAS RUIDO
NI_c1=10*log10(interferencia_c1_v + pn_v);
NI_c2=10*log10(interferencia_c2_v + pn_v);
NI_c3=10*log10(interferencia_c3_v + pn_v);
NI_c4=10*log10(interferencia_c4_v + pn_v);


%% Calculo de SINR
switch desvanecimiento
    
    case 2
    SINR_c1(:,NumSim)= prx1_des_l-NI_c1';     % Valores de SINR para los UEs de la celda 1
    SINR_c2(:,NumSim)= prx2_des_l-NI_c2';     % Valores de SINR para los UEs de la celda 2
    SINR_c3(:,NumSim)= prx3_des_l-NI_c3';     % Valores de SINR para los UEs de la celda 3
    SINR_c4(:,NumSim)= prx4_des_l-NI_c4';     % Valores de SINR para los UEs de la celda 4 
    
    SINR=[SINR_c1(:,NumSim) SINR_c2(:,NumSim) SINR_c3(:,NumSim) SINR_c4(:,NumSim)];

    PRX1(:,NumSim)=prx1_des_l;       % Valores de Prx para los UEs de la celda 1
    PRX2(:,NumSim)=prx2_des_l;       % Valores de Prx para los UEs de la celda 2
    PRX3(:,NumSim)=prx3_des_l;       % Valores de Prx para los UEs de la celda 3
    PRX4(:,NumSim)=prx4_des_l;       % Valores de Prx para los UEs de la celda 4

    case 3      
    SINR_c1(:,NumSim)= prx1_des_rl-NI_c1';     % Valores de SINR para los UEs de la celda 1
    SINR_c2(:,NumSim)= prx2_des_rl-NI_c2';     % Valores de SINR para los UEs de la celda 2
    SINR_c3(:,NumSim)= prx3_des_rl-NI_c3';     % Valores de SINR para los UEs de la celda 3
    SINR_c4(:,NumSim)= prx4_des_rl-NI_c4';     % Valores de SINR para los UEs de la celda 4 
          
    SINR=[SINR_c1(:,NumSim) SINR_c2(:,NumSim) SINR_c3(:,NumSim) SINR_c4(:,NumSim)];
      
    PRX1(:,NumSim)=prx1_des_rl;       % Valores de Prx para los UEs de la celda 1
    PRX2(:,NumSim)=prx2_des_rl;       % Valores de Prx para los UEs de la celda 2
    PRX3(:,NumSim)=prx3_des_rl;       % Valores de Prx para los UEs de la celda 3
    PRX4(:,NumSim)=prx4_des_rl;       % Valores de Prx para los UEs de la celda 4
        
    case 4
    SINR_c1(:,NumSim)= prx1-NI_c1';     % Valores de SINR para los UEs de la celda 1
    SINR_c2(:,NumSim)= prx2-NI_c2';     % Valores de SINR para los UEs de la celda 2
    SINR_c3(:,NumSim)= prx3-NI_c3';     % Valores de SINR para los UEs de la celda 3
    SINR_c4(:,NumSim)= prx4-NI_c4';     % Valores de SINR para los UEs de la celda 4 
    
    SINR=[SINR_c1(:,NumSim) SINR_c2(:,NumSim) SINR_c3(:,NumSim) SINR_c4(:,NumSim)];

    PRX1(:,NumSim)=prx1;       % Valores de Prx para los UEs de la celda 1
    PRX2(:,NumSim)=prx2;       % Valores de Prx para los UEs de la celda 2
    PRX3(:,NumSim)=prx3;       % Valores de Prx para los UEs de la celda 3
    PRX4(:,NumSim)=prx4;       % Valores de Prx para los UEs de la celda 4      
end   


%% Asignaci�n del CQI 
[cqi]=indice_cqi(3*nues,SINR);

% Asignaci�n Indice TBS 
tabla_itbs= xlsread('CQI.xls');
tbs=zeros(3*nues,4);

min=tabla_itbs(minMR+1,4);
minSINR=tabla_itbs(minMR+2,2);

for j2=1:3*nues 
for i2=1:4 
tbs(j2,i2)=tabla_itbs(cqi(j2,i2)+1,4);       
end
end

%% asignaci�n de recursos
switch planificador
    
 case 2 %%Estrategia de planificaci�n Round Robin(RR)   
        
    [prb_RR,prb_unused]=plan_Round_Robin(nc,tp_RR,prb,3*nues);
    tabla_capacidad= xlsread('capacidad.xls');
    
    for i=1:3*nues 
    for j=1:4 
    throughput_RR(i,j)=tabla_capacidad(tbs(i,j)+2,prb_RR(i,j)+1);   
    end
    end
    
    RR1(:,NumSim)=prb_RR(:,1);
    RR2(:,NumSim)=prb_RR(:,2);
    RR3(:,NumSim)=prb_RR(:,3);
    RR4(:,NumSim)=prb_RR(:,4);
            
    tp_RR=sum(throughput_RR)/3*nues;
    
 case 3 %%Estrategia de planificaci�n Proportional Fair(PF)   
        
    [prb_PF]=plan_Proportional_Fair(nc,tp_PF,tbs,SINR,prb,3*nues);
    archivo_tbs=strcat(nombre_secuencia_tbs, num2str(NumSim),'.txt')
    archivo_snr=strcat(nombre_secuencia_snr, num2str(NumSim),'.txt')
    prbs_archivo=strcat(nombre_secuencia_prb, num2str(NumSim),'.txt')
    %tbs;
    
    fid = fopen(prbs_archivo, 'wt');
    fprintf(fid,'%f %f %f %f\n',[prb_PF(:,1),prb_PF(:,2),prb_PF(:,3),prb_PF(:,4)]);
    fid = fclose(fid);
    
    fid = fopen(archivo_snr, 'wt');
    fprintf(fid,'%f %f %f %f\n',[SINR(:,1),SINR(:,2),SINR(:,3),SINR(:,4)]);
    fid = fclose(fid);
    
    fid = fopen(archivo_tbs, 'wt');
    fprintf(fid,'%f %f %f %f\n',[tbs(:,1), tbs(:,2), tbs(:,3), tbs(:,4)]);
    fid = fclose(fid);
    prb_PF=load('ganadores.txt');
    tbs=load('tbs1.txt');
    %save -ascii archivo_tbs tbs;
    tabla_capacidad= xlsread('capacidad.xls');
    for i=1:3*nues 
    for j=1:4
    throughput_PF(i,j)=tabla_capacidad(tbs(i,j)+2,prb_PF(i,j)+1);
    throughput_PF(i,j)
    end
    end

    PF1(:,NumSim)=prb_PF(:,1);
    PF2(:,NumSim)=prb_PF(:,2);
    PF3(:,NumSim)=prb_PF(:,3);
    PF4(:,NumSim)=prb_PF(:,4);
    %PF1
    %PF2
    %PF3
    %PF4
    tp_PF=sum(throughput_PF)/3*nues;
 case 4 %%Estrategia de planificaci�n Maximun Rate (MR)   
        
    [prb_MR]=plan_Maximun_Rate(nc,min,tbs,SINR,prb,3*nues);
        
    tabla_capacidad= xlsread('capacidad.xls');
    for i=1:3*nues 
    for j=1:4 
    throughput_MR(i,j)=tabla_capacidad(tbs(i,j)+2,prb_MR(i,j)+1);   
    end
    end
    
    MR1(:,NumSim)=prb_MR(:,1);
    MR2(:,NumSim)=prb_MR(:,2);
    MR3(:,NumSim)=prb_MR(:,3);
    MR4(:,NumSim)=prb_MR(:,4);
 case 5 %%Estrategias de plnificaci�n RR,PF y MR simult�neamente
    
    [prb_RR,prb_unused]=plan_Round_Robin(nc,tp_RR,prb,3*nues);
    [prb_PF]=plan_Proportional_Fair(nc,tp_PF,tbs,SINR,prb,3*nues);
    [prb_MR]=plan_Maximun_Rate(nc,min,tbs,SINR,prb,3*nues);
      
    tabla_capacidad= xlsread('capacidad.xls');
    for i=1:3*nues 
    for j=1:4 
    throughput_RR(i,j)=tabla_capacidad(tbs(i,j)+2,prb_RR(i,j)+1);
    throughput_PF(i,j)=tabla_capacidad(tbs(i,j)+2,prb_PF(i,j)+1); 
    throughput_MR(i,j)=tabla_capacidad(tbs(i,j)+2,prb_MR(i,j)+1); 
    end
    end
    
    RR1(:,NumSim)=prb_RR(:,1);
    RR2(:,NumSim)=prb_RR(:,2);
    RR3(:,NumSim)=prb_RR(:,3);
    RR4(:,NumSim)=prb_RR(:,4);
    
    PF1(:,NumSim)=prb_PF(:,1);
    PF2(:,NumSim)=prb_PF(:,2);
    PF3(:,NumSim)=prb_PF(:,3);
    PF4(:,NumSim)=prb_PF(:,4);
    
    MR1(:,NumSim)=prb_MR(:,1);
    MR2(:,NumSim)=prb_MR(:,2);
    MR3(:,NumSim)=prb_MR(:,3);
    MR4(:,NumSim)=prb_MR(:,4);
    
    tp_RR=sum(throughput_RR)/3*nues;
    tp_PF=sum(throughput_PF)/3*nues;
end
%-------------------------------------------------------------------------------------------------
%% Algoritmo de PC
%Perdidas de Trayectoria PL
PL = PtxENB - [PRX1(:,NumSim), PRX2(:,NumSim), PRX3(:,NumSim) , PRX4(:,NumSim)]; %db  De acuerdo al desvanecimiento
%Potencia de Tx del UE OLPC
x=zeros(1,3*nues); %indica el tama�o de la estructura
Celdas =struct('Celda1',x,'Celda2',x,'Celda3',x,'Celda4',x);
switch planificador
    case 2
        prbOLPC=prb_RR;
        Celdas.Celda1=subportadora(prb_RR(:,1),nues);
        Celdas.Celda2=subportadora(prb_RR(:,2),nues);
        Celdas.Celda3=subportadora(prb_RR(:,3),nues);
        Celdas.Celda4=subportadora(prb_RR(:,4),nues);
        
    case 3
        prbOLPC=prb_PF;
        Celdas.Celda1=subportadora(prb_PF(:,1),nues);
        Celdas.Celda2=subportadora(prb_PF(:,2),nues);
        Celdas.Celda3=subportadora(prb_PF(:,3),nues);
        Celdas.Celda4=subportadora(prb_PF(:,4),nues);
    case 4 
        prbOLPC=prb_MR;
        Celdas.Celda1=subportadora(prb_MR(:,1),nues);
        Celdas.Celda2=subportadora(prb_MR(:,2),nues);
        Celdas.Celda3=subportadora(prb_MR(:,3),nues);
        Celdas.Celda4=subportadora(prb_MR(:,4),nues);
    case 5
        prbOLPC=prb_RR;
        Celdas.Celda1=subportadora(prb_RR(:,1),nues);
        Celdas.Celda2=subportadora(prb_RR(:,2),nues);
        Celdas.Celda3=subportadora(prb_RR(:,3),nues);
        Celdas.Celda4=subportadora(prb_RR(:,4),nues);
end
%%Calculo y Validacion de la PTx del UE
if (NumSim == 1)
    %PtxUE es la potencia de transmision del UE con los pasos, Pmax es una estructura que indica si el UE ha alcanzado la potencia maxima 
    [PtxUE,Pmax(NumSim).ue,PtxolPL] = ObtenerPtxUE(prbOLPC,Po,alpha,PL,pasos); %  En este caso los pasos son la matrix de ceros
else
    %Este procedimiento se agrega un paso de 2db a los UE que no alcanzan la SINR objetivo y todavia pueden aumentar la Ptx en caso que ya esten transmitiendo con Ptmax se deja desconectado al UE
    %pst hace el cambio de la matrix de servicio pasando los unos a ceros y los ceros a uno (estos seran los pasos).
    pst =Service(NumSim-1).ue*3;
    pst2=pst;
    pst2(pst2<2)=2; %tama�o del paso 2db
    pst2(pst2==3)=0;
    Pstep(NumSim).ue = pst2; %Matrix de pasos
    potenciamax = Pmax(NumSim-1).ue; % Matrix que indica que UE alcanzaron la Ptxmax en la iteraci�n anterior.
    ser = Service(NumSim-1).ue; %Se indica quien tuvo servicio en la iteracion anterior.
    trans = PTXUEol(NumSim-1).ue; %indica la potencia de transmisi�n del UE en OL en la iteraci�n anterior.
   
    for i=1:3*nues
        for j=1:nc
        if(trans(i,j) == 0 ||potenciamax(i,j) == 1 && ser(i,j)==0)
            potenciaol(i,j)=0; % el cero indica que el UE no transmite porque asi transmita con Pmax no se conecta al eNB.
        else
            potenciaol(i,j)=1;
        end
        end
    end
    pasos = pasos + Pstep(NumSim).ue; 
    [Pmmm,Pmax(NumSim).ue,PtxolPL] = ObtenerPtxUE(prbOLPC,Po,alpha,PL,pasos);
    PtxUE = Pmmm.*potenciaol;
end
PTXUEol(NumSim).ue = PtxUE;
%--------------------------------------------------------------------------------------------------------------------------------------
%% Calculo de potencias recibidas en el eNB de los UEs de su celda
% Celda1
[prx, pdl, pdr]=pot_celdaup(1, 3*nues, Lup1, PtxUE);
prxup1=prx;
prxup1_des_l=pdl;
prxup1_des_rl=pdr;

% Celda2
[prx, pdl, pdr]=pot_celdaup(2, 3*nues, Lup2, PtxUE);
prxup2=prx;
prxup2_des_l=pdl;
prxup2_des_rl=pdr;

% Celda3
[prx, pdl, pdr]=pot_celdaup(3, 3*nues, Lup3, PtxUE);
prxup3=prx;
prxup3_des_l=pdl;
prxup3_des_rl=pdr;

% Celda4
[prx, pdl, pdr]=pot_celdaup(4, 3*nues, Lup4,PtxUE);
prxup4=prx;
prxup4_des_l=pdl;
prxup4_des_rl=pdr;

%%Interferencia en Uplink
%Identificacion de los UE interferentes deacuerdo al subconjunto de subportadoras

%Interferencia para UE Celda1 (Matriz(#UExcelda,#UExcelda))
Celda1_C2= InterfeUp(Celdas.Celda1,Celdas.Celda2,3*nues);
Celda1_C3= InterfeUp(Celdas.Celda1,Celdas.Celda3,3*nues);
Celda1_C4= InterfeUp(Celdas.Celda1,Celdas.Celda4,3*nues);
IntCelda.Celda1=intCeltotal( Celda1_C2,Celda1_C3,Celda1_C4,3*nues);

%Interferencia para UE Celda2
Celda2_C1= InterfeUp(Celdas.Celda2,Celdas.Celda1,3*nues);
Celda2_C3= InterfeUp(Celdas.Celda2,Celdas.Celda3,3*nues);
Celda2_C4= InterfeUp(Celdas.Celda2,Celdas.Celda4,3*nues);
IntCelda.Celda2=intCeltotal( Celda2_C1,Celda2_C3,Celda2_C4,3*nues);

%Interferencia para UE Celda3
Celda3_C1= InterfeUp(Celdas.Celda3,Celdas.Celda1,3*nues);
Celda3_C2= InterfeUp(Celdas.Celda3,Celdas.Celda2,3*nues);
Celda3_C4= InterfeUp(Celdas.Celda3,Celdas.Celda4,3*nues);
IntCelda.Celda3=intCeltotal( Celda3_C1,Celda3_C2,Celda3_C4,3*nues);

%Interferencia para UE Celda4
Celda4_C1= InterfeUp(Celdas.Celda4,Celdas.Celda1,3*nues);
Celda4_C2= InterfeUp(Celdas.Celda4,Celdas.Celda2,3*nues);
Celda4_C3= InterfeUp(Celdas.Celda4,Celdas.Celda3,3*nues); 
IntCelda.Celda4=intCeltotal( Celda4_C1,Celda4_C2,Celda4_C3,3*nues);
%------------------------------------------------------------------------------------
%% Calculo de perdidas de propagacion de las se�ales interferentes
%Perdidas de UE de otras celdas hacia el eNB1 (Celda 1).
    Lup_1=[Lup2(:,1) Lup3(:,1) Lup4(:,1)];
%Potencia de TX de UE interferentes a la Celda1.
    Pintup_1 = [PtxUE(:,2) PtxUE(:,3) PtxUE(:,4)];
    
%Perdidas de UE de otras celdas hacia el eNB2 (Celda 2).
    Lup_2=[Lup1(:,2) Lup3(:,2) Lup4(:,2)];
%Potencia de TX de UE interferentes a la Celda2.
    Pintup_2 = [PtxUE(:,1) PtxUE(:,3) PtxUE(:,4)];
    
%Perdidas de UE de otras celdas hacia el eNB3 (Celda 3).
    Lup_3=[Lup1(:,3) Lup2(:,3) Lup4(:,3)];
%Potencia de TX de UE interferentes a la Celda3.
    Pintup_3 = [PtxUE(:,1) PtxUE(:,2) PtxUE(:,4)];
    
%Perdidas de UE de otras celdas hacia el eNB4 (Celda 4).
    Lup_4=[Lup1(:,4) Lup2(:,4) Lup3(:,4)];
%Potencia de TX de UE interferentes a la Celda1.
    Pintup_4 = [PtxUE(:,1) PtxUE(:,2) PtxUE(:,3)];
       
%% CALCULO DE LA POTENCIA DE Rx Interferente.
%en esta parte se calcula las potencias recibidas interferentes para cada
%UE sin desvanecimiento y con desvanecimiento rapido y lento.
%Celda1
[PotintCelda1]=Potup_Int(nc,3*nues, Lup_1, Pintup_1,IntCelda.Celda1);

%Celda2
[PotintCelda2]=Potup_Int(nc,3*nues, Lup_2, Pintup_2,IntCelda.Celda2);

%Celda3
[PotintCelda3]=Potup_Int(nc,3*nues, Lup_3, Pintup_3,IntCelda.Celda3);

%Celda4
[PotintCelda4]=Potup_Int(nc,3*nues, Lup_4, Pintup_4,IntCelda.Celda4);
%--------------------------------------------------------------------------------------------
%Suma de potencias interferentes para cada UE para cada tipo de
%desvanecimiento
InterferenciaTotal= SumInt(PotintCelda1,PotintCelda2,PotintCelda3,PotintCelda4,3*nues);
%-----------------------------------------------------------------------------------------
switch desvanecimiento
  case 2
  interferenciaup = InterferenciaTotal.lento;
  PRXup1(:,NumSim)= prxup1_des_l;       % Valores de Prx de los UEs en el eNB1
  PRXup2(:,NumSim)= prxup2_des_l;       % Valores de Prx de los UEs en el eNB2
  PRXup3(:,NumSim)= prxup3_des_l;       % Valores de Prx de los UEs en el eNB3
  PRXup4(:,NumSim)= prxup4_des_l;       % Valores de Prx de los UEs en el eNB4
  
  case 3      
  interferenciaup = InterferenciaTotal.rapido;
  PRXup1(:,NumSim)= prxup1_des_rl;       % Valores de Prx de los UEs en el eNB1
  PRXup2(:,NumSim)= prxup2_des_rl;       % Valores de Prx de los UEs en el eNB2
  PRXup3(:,NumSim)= prxup3_des_rl;       % Valores de Prx de los UEs en el eNB3
  PRXup4(:,NumSim)= prxup4_des_rl;       % Valores de Prx de los UEs en el eNB4
  
  case 4
  interferenciaup = InterferenciaTotal.sin;    
  PRXup1(:,NumSim)= prxup1;       % Valores de Prx de los UEs en el eNB1
  PRXup2(:,NumSim)= prxup2;       % Valores de Prx de los UEs en el eNB2
  PRXup3(:,NumSim)= prxup3;       % Valores de Prx de los UEs en el eNB3
  PRXup4(:,NumSim)= prxup4;       % Valores de Prx de los UEs en el eNB4
end 

%% Calculo interferencias totales hacia los usuarios del Sistema  MAS RUIDO
%Ruido del sistema
switch planificador
    case 2
        nsys = Pnoise(prb_RR);
    case 3
        nsys = Pnoise(prb_PF);     
    case 4 
        nsys = Pnoise(prb_MR);
    case 5
        nsys = Pnoise(prb_RR);
end
%--------------------------------------------------------
NIup = zeros(3*nues,nc);
for i=1:3*nues
    for j=1:nc
        if(interferenciaup(i,j)==0 && nsys(i,j)==0 || PtxUE(i,j)==0)
            NIup(i,j)=0;
        else
            NIup(i,j)=10*log10(interferenciaup(i,j)+nsys(i,j));
        end
    end
end
%% Calculo de SINR en UL
switch desvanecimiento

    case 2    
    SINRup_c1(:,NumSim)= prxup1_des_l-NIup(:,1);     % Valores de SINR para los UEs de la celda 1
    SINRup_c2(:,NumSim)= prxup2_des_l-NIup(:,2);     % Valores de SINR para los UEs de la celda 2
    SINRup_c3(:,NumSim)= prxup3_des_l-NIup(:,3);     % Valores de SINR para los UEs de la celda 3
    SINRup_c4(:,NumSim)= prxup4_des_l-NIup(:,4);     % Valores de SINR para los UEs de la celda 4  
    SINRup=[SINRup_c1(:,NumSim) SINRup_c2(:,NumSim) SINRup_c3(:,NumSim) SINRup_c4(:,NumSim)];
    
    case 3
    SINRup_c1(:,NumSim)= prxup1_des_rl-NIup(:,1);     % Valores de SINR para los UEs de la celda 1
    SINRup_c2(:,NumSim)= prxup2_des_rl-NIup(:,2);     % Valores de SINR para los UEs de la celda 2
    SINRup_c3(:,NumSim)= prxup3_des_rl-NIup(:,3);     % Valores de SINR para los UEs de la celda 3
    SINRup_c4(:,NumSim)= prxup4_des_rl-NIup(:,4);     % Valores de SINR para los UEs de la celda 4
    SINRup=[SINRup_c1(:,NumSim) SINRup_c2(:,NumSim) SINRup_c3(:,NumSim) SINRup_c4(:,NumSim)];
              
    case 4
    SINRup_c1(:,NumSim)= prxup1-NIup(:,1);     % Valores de SINR para los UEs de la celda 1
    SINRup_c2(:,NumSim)= prxup2-NIup(:,2);     % Valores de SINR para los UEs de la celda 2
    SINRup_c3(:,NumSim)= prxup3-NIup(:,3);     % Valores de SINR para los UEs de la celda 3
    SINRup_c4(:,NumSim)= prxup4-NIup(:,4);     % Valores de SINR para los UEs de la celda 4 
    SINRup=[SINRup_c1(:,NumSim) SINRup_c2(:,NumSim) SINRup_c3(:,NumSim) SINRup_c4(:,NumSim)];
end
SINRol(NumSim).ue= SINRup;
%%Revisar si se alcanzo la SINR objetivo con lazo abierto para pasar a lazo cerrado
%Distancia de los UE de la celda i al eNB i.
dist = [dist_bs1(:,1) dist_bs2(:,2) dist_bs3(:,3) dist_bs4(:,4)];
%%Calculo de Servicio
[Servicioup,UEsiup,UEnoup,disUE] = servicio(SNRo,SINRup,dist,PtxUE);
%Guardo matriz de servicio para tener en cuenta cuando se conecto el UE.
Service(NumSim).ue = Servicioup;
%Si se encuentra en servicio guardo el valor del paso
for i=1:3*nues
    for j=1:nc
        if (Servicioup(i,j)==1 && savestep(i,j)==0) %Si tiene servicio el UE y no tiene valor de paso guardado alguna de las iteraciones
            savestep(i,j)= pasos(i,j);%guardo el valor de la sumatoria de  pasos con que alcanzo servicio
        end
        if (serviciocte(i,j)==0)%Variable serviciocte se pone en uno cuando a la primera vez tiene servicio el UE
            serviciocte(i,j)=Servicioup(i,j);
        end
    end
end
if (NumSim == 1)
    Ptransmision(NumSim).ue = PtxUE; % En la primera iteraci�n la potencia transmitida es obligatoriamente calculada con lazo abierto
else
    [Ptransmision(NumSim).ue, compc(NumSim).com ] = calculoPTRXCL(serviciocte,ServicioCL(NumSim-1).ue,PtxUE,PtxolPL,Ptransmision(NumSim-1).ue,comTPC,NumSim,compc,savestep,SNRo,SINRcl(NumSim-1).ue);
end
PtxUEclpc = Ptransmision(NumSim).ue;

%% Calculo de potencias recibidas en el eNB de los UEs de su celda
% Celda1
[prx, pdl, pdr]=pot_celdaup(1, 3*nues, Lup1, PtxUEclpc);
prxup1cl=prx;
prxup1cl_des_l=pdl;
prxup1cl_des_rl=pdr;

% Celda2
[prx, pdl, pdr]=pot_celdaup(2, 3*nues, Lup2, PtxUEclpc);
prxup2cl=prx;
prxup2cl_des_l=pdl;
prxup2cl_des_rl=pdr;

% Celda3
[prx, pdl, pdr]=pot_celdaup(3, 3*nues, Lup3, PtxUEclpc);
prxup3cl=prx;
prxup3cl_des_l=pdl;
prxup3cl_des_rl=pdr;

% Celda4
[prx, pdl, pdr]=pot_celdaup(4, 3*nues, Lup4,PtxUEclpc);
prxup4cl=prx;
prxup4cl_des_l=pdl;
prxup4cl_des_rl=pdr;

%% Calculo de perdidas de propagacion de las se�ales interferentes
%Potencia de TX de UE interferentes a la Celda1.
    Pintupcl_1 = [PtxUEclpc(:,2) PtxUEclpc(:,3) PtxUEclpc(:,4)];
%Potencia de TX de UE interferentes a la Celda2.
    Pintupcl_2 = [PtxUEclpc(:,1) PtxUEclpc(:,3) PtxUEclpc(:,4)];
%Potencia de TX de UE interferentes a la Celda3.
    Pintupcl_3 = [PtxUEclpc(:,1) PtxUEclpc(:,2) PtxUEclpc(:,4)];
%Potencia de TX de UE interferentes a la Celda1.
    Pintupcl_4 = [PtxUEclpc(:,1) PtxUEclpc(:,2) PtxUEclpc(:,3)];
       
%% CALCULO DE LA POTENCIA DE Rx Interferente.
%Celda1
[PotintCelda1cl] = Potup_Int(nc,3*nues, Lup_1, Pintupcl_1,IntCelda.Celda1);

%Celda2
[PotintCelda2cl] = Potup_Int(nc,3*nues, Lup_2, Pintupcl_2,IntCelda.Celda2);

%Celda3
[PotintCelda3cl] = Potup_Int(nc,3*nues, Lup_3, Pintupcl_3,IntCelda.Celda3);

%Celda4
[PotintCelda4cl] = Potup_Int(nc,3*nues, Lup_4, Pintupcl_4,IntCelda.Celda4);
%--------------------------------------------------------------------------------------------
%Suma de potencias interferentes para cada UE para cada tipo de
%desvanecimiento
InterferenciaTotalcl= SumInt(PotintCelda1cl,PotintCelda2cl,PotintCelda3cl,PotintCelda4cl,3*nues);

switch desvanecimiento
    
  case 2
  interferenciaupcl = InterferenciaTotalcl.lento;
  PRXup1cl(:,NumSim)=prxup1cl_des_l;       % Valores de Prx de los UEs en el eNB1
  PRXup2cl(:,NumSim)=prxup2cl_des_l;       % Valores de Prx de los UEs en el eNB2
  PRXup3cl(:,NumSim)=prxup3cl_des_l;       % Valores de Prx de los UEs en el eNB3
  PRXup4cl(:,NumSim)=prxup4cl_des_l;       % Valores de Prx de los UEs en el eNB4
  
  case 3      
  interferenciaupcl = InterferenciaTotalcl.rapido;
  PRXup1cl(:,NumSim)=prxup1cl_des_rl;       % Valores de Prx de los UEs en el eNB1
  PRXup2cl(:,NumSim)=prxup2cl_des_rl;       % Valores de Prx de los UEs en el eNB2
  PRXup3cl(:,NumSim)=prxup3cl_des_rl;       % Valores de Prx de los UEs en el eNB3
  PRXup4cl(:,NumSim)=prxup4cl_des_rl;       % Valores de Prx de los UEs en el eNB4
  
  case 4
  interferenciaupcl = InterferenciaTotalcl.sin;    
  PRXup1cl(:,NumSim)=prxup1cl;       % Valores de Prx de los UEs en el eNB1
  PRXup2cl(:,NumSim)=prxup2cl;       % Valores de Prx de los UEs en el eNB2
  PRXup3cl(:,NumSim)=prxup3cl;       % Valores de Prx de los UEs en el eNB3
  PRXup4cl(:,NumSim)=prxup4cl;       % Valores de Prx de los UEs en el eNB4
end 

%% Calculo interferencias totales hacia los usuarios del Sistema  MAS RUIDO
NIupcl = zeros(3*nues,nc);
for i=1:3*nues
    for j=1:nc
        if(interferenciaupcl(i,j)==0 && nsys(i,j)==0 || PtxUEclpc(i,j)==0)
            NIupcl(i,j)=0;
        else
            NIupcl(i,j)=10*log10(interferenciaupcl(i,j)+nsys(i,j));
        end
    end
end
%% Calculo de SINR en UL
switch desvanecimiento
    
    case 2    
    SINRupcl_c1(:,NumSim)= prxup1cl_des_l-NIupcl(:,1);     % Valores de SINR para los UEs de la celda 1
    SINRupcl_c2(:,NumSim)= prxup2cl_des_l-NIupcl(:,2);     % Valores de SINR para los UEs de la celda 2
    SINRupcl_c3(:,NumSim)= prxup3cl_des_l-NIupcl(:,3);     % Valores de SINR para los UEs de la celda 3
    SINRupcl_c4(:,NumSim)= prxup4cl_des_l-NIupcl(:,4);     % Valores de SINR para los UEs de la celda 4 
    SINRupcl=[SINRupcl_c1(:,NumSim) SINRupcl_c2(:,NumSim) SINRupcl_c3(:,NumSim) SINRupcl_c4(:,NumSim)];
    
    case 3
    SINRupcl_c1(:,NumSim)= prxup1cl_des_rl-NIupcl(:,1);     % Valores de SINR para los UEs de la celda 1
    SINRupcl_c2(:,NumSim)= prxup2cl_des_rl-NIupcl(:,2);     % Valores de SINR para los UEs de la celda 2
    SINRupcl_c3(:,NumSim)= prxup3cl_des_rl-NIupcl(:,3);     % Valores de SINR para los UEs de la celda 3
    SINRupcl_c4(:,NumSim)= prxup4cl_des_rl-NIupcl(:,4);     % Valores de SINR para los UEs de la celda 4   
    SINRupcl=[SINRupcl_c1(:,NumSim) SINRupcl_c2(:,NumSim) SINRupcl_c3(:,NumSim) SINRupcl_c4(:,NumSim)];
              
    case 4
    SINRupcl_c1(:,NumSim)= prxup1cl-NIupcl(:,1);     % Valores de SINR para los UEs de la celda 1
    SINRupcl_c2(:,NumSim)= prxup2cl-NIupcl(:,2);     % Valores de SINR para los UEs de la celda 2
    SINRupcl_c3(:,NumSim)= prxup3cl-NIupcl(:,3);     % Valores de SINR para los UEs de la celda 3
    SINRupcl_c4(:,NumSim)= prxup4cl-NIupcl(:,4);     % Valores de SINR para los UEs de la celda 4 
    SINRupcl=[SINRupcl_c1(:,NumSim) SINRupcl_c2(:,NumSim) SINRupcl_c3(:,NumSim) SINRupcl_c4(:,NumSim)];
end   

%Guardo la SINR de lazo cerrado para seguir realizando los calculos de lazo cerrado en cada iteracion 
SINRcl(NumSim).ue= SINRupcl;
[Servicioupcl, UEsiupcl,UEnoupcl, disUEcl ] = servicio(SNRo,SINRupcl,dist,PtxUEclpc); %si no ptx no servicio y evaluacion de sinr vs sinrtarget
ServicioCL(NumSim).ue = Servicioupcl;
%% Asignaci�n del CQI Se utiliza la misma tabla de DL
[cqiup]=indice_cqi(3*nues,SINRup);
[cqiupcl]=indice_cqi(3*nues,SINRupcl);

%% Asignaci�n Indice TBS (se utiliza la tabla de UL)
tabla_itbs= xlsread('CQIup.xls');
tbsup=zeros(3*nues,4);
tbsupcl=zeros(3*nues,4);
for j2=1:3*nues 
for i2=1:nc 
   tbsup(j2,i2)=tabla_itbs(cqiup(j2,i2)+1,4);
   tbsupcl(j2,i2)=tabla_itbs(cqiupcl(j2,i2)+1,4);    
end
end

%%SchedulingPF
[prb_PFup]=plan_Proportional_FairUP(Servicioup,tbsup,SINRup,tp_PFup); 
[prb_PFupcl]=plan_Proportional_FairUP(Servicioupcl,tbsupcl,SINRupcl,tp_PFup);       

tabla_capacidad= xlsread('capacidad.xls'); 
throughput_PFup = zeros(3*nues,4);
throughput_PFupcl = zeros(3*nues,4);

%Promedio de UE activos en cada celda
proUEactivosC = sum(sum(Servicioup))/4;
proUEactivosCcl = sum(sum(Servicioupcl))/4;

    for i=1:3*nues 
        for j=1:4
            if (PtxUE(i,j)==0 || prb_PFup(i,j)==0||Servicioup(i,j)==0)
                throughput_PFup(i,j)=0;
            else
                throughput_PFup(i,j)=tabla_capacidad(tbsup(i,j)+2,prb_PFup(i,j)+1);   
            end
            if (PtxUEclpc(i,j)==0 || prb_PFupcl(i,j)==0||Servicioupcl(i,j)==0)
                throughput_PFupcl(i,j)=0;
            else
                throughput_PFupcl(i,j)=tabla_capacidad(tbsupcl(i,j)+2,prb_PFupcl(i,j)+1);   
            end
        end
    end
%qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
%%Asignaci�n de Recursos uplink
    PF1up(:,NumSim)=prb_PFup(:,1);
    PF2up(:,NumSim)=prb_PFup(:,2);
    PF3up(:,NumSim)=prb_PFup(:,3);
    PF4up(:,NumSim)=prb_PFup(:,4);
%qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
    tp_PFup = sum(throughput_PFup)/ceil(proUEactivosC);
    throughput_c1_PFup(:,NumSim)=(throughput_PFup(:,1))/1e3;
    throughput_c2_PFup(:,NumSim)=(throughput_PFup(:,2))/1e3;
    throughput_c3_PFup(:,NumSim)=(throughput_PFup(:,3))/1e3;
    throughput_c4_PFup(:,NumSim)=(throughput_PFup(:,4))/1e3;%En Mbps
    %---------------------------------------------------------------------------
    %qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
%%Asignaci�n de Recursos uplink
    PF1upcl(:,NumSim)=prb_PFupcl(:,1);
    PF2upcl(:,NumSim)=prb_PFupcl(:,2);
    PF3upcl(:,NumSim)=prb_PFupcl(:,3);
    PF4upcl(:,NumSim)=prb_PFupcl(:,4);
    %qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
    tp_PFupcl = sum(throughput_PFupcl)/ceil(proUEactivosCcl);
    throughput_c1_PFupcl(:,NumSim)=(throughput_PFupcl(:,1))/1e3;
    throughput_c2_PFupcl(:,NumSim)=(throughput_PFupcl(:,2))/1e3;
    throughput_c3_PFupcl(:,NumSim)=(throughput_PFupcl(:,3))/1e3;
    throughput_c4_PFupcl(:,NumSim)=(throughput_PFupcl(:,4))/1e3;%En Mbps
    
%Calculo de distancia maxima de servicio de cada celda en Km
Radio1(:,NumSim) = max(disUE(:,1));
Radio2(:,NumSim) = max(disUE(:,2));
Radio3(:,NumSim) = max(disUE(:,3));
Radio4(:,NumSim) = max(disUE(:,4));

Radio1cl(:,NumSim) = max(disUEcl(:,1));
Radio2cl(:,NumSim) = max(disUEcl(:,2));
Radio3cl(:,NumSim) = max(disUEcl(:,3));
Radio4cl(:,NumSim) = max(disUEcl(:,4));

%Probabilidad de Servicio
Probabilidad(:,NumSim) = 100*UEsiup/(nc*nues*3);
Probabilidadcl(:,NumSim) = 100*UEsiupcl/(nc*nues*3);

%%
% 
throughput_c1_RR(:,NumSim)=(throughput_RR(:,1))/1e3;
throughput_c1_PF(:,NumSim)=(throughput_PF(:,1))/1e3;
throughput_c1_MR(:,NumSim)=(throughput_MR(:,1))/1e3;% en Mbps

throughput_c2_RR(:,NumSim)=(throughput_RR(:,2))/1e3;
throughput_c2_PF(:,NumSim)=(throughput_PF(:,2))/1e3;
throughput_c2_MR(:,NumSim)=(throughput_MR(:,2))/1e3;% en Mbps

throughput_c3_RR(:,NumSim)=(throughput_RR(:,3))/1e3;
throughput_c3_PF(:,NumSim)=(throughput_PF(:,3))/1e3;
throughput_c3_MR(:,NumSim)=(throughput_MR(:,3))/1e3;% en Mbps

throughput_c4_RR(:,NumSim)=(throughput_RR(:,4))/1e3;
throughput_c4_PF(:,NumSim)=(throughput_PF(:,4))/1e3;
throughput_c4_MR(:,NumSim)=(throughput_MR(:,4))/1e3;% en Mbps
 
if (NumSim==1)                    
SINR_T=SINR;
else
SINR_T = [SINR_T;SINR];
end
run 'Cargando'
end
%----------------------------------------------------------
%Radios promedios de Cobertura en cada Celda OLPC
rdup1 = sum(Radio1)/rept;
rdup2 = sum(Radio2)/rept;
rdup3 = sum(Radio3)/rept;
rdup4 = sum(Radio4)/rept;

%Radios promedios de Cobertura en cada Celda CLPC
rdup1cl = sum(Radio1cl)/rept;
rdup2cl = sum(Radio2cl)/rept;
rdup3cl = sum(Radio3cl)/rept;
rdup4cl = sum(Radio4cl)/rept;

RadiosCobertura = [rdup1 rdup2 rdup3 rdup4];
RadiosCoberturacl = [rdup1cl rdup2cl rdup3cl rdup4cl];

%Probabilidad de Servicio del Sistema
Prob = sum(Probabilidad)/rept;
Probcl =sum(Probabilidadcl)/rept;

%Probabilidad de servicio del UE por Celda
servi =zeros(3*nues,nc);
servicl =zeros(3*nues,nc);
for i=1:rept
    servi=servi+Service(i).ue;
    servicl=servicl+ServicioCL(i).ue;
end

seup = zeros(3*nues,nc);
seupcl=zeros(3*nues,nc);
for i=1:nc
    for j=1:3*nues
        if servi(j,i)> CoberUE
            seup(j,i) = 1; %el UE tiene servicio
        else
            seup(j,i) = 0; %el UE no tiene servicio
        end
        
        if servicl(j,i)> CoberUE
            seupcl(j,i) = 1; %el UE tiene servicio
        else
            seupcl(j,i) = 0; %el UE no tiene servicio
        end 
    end
end

%Esto es para borrar
repeticion = 1:1:rept;
mediaprool= mean(Probabilidad);
mediaprocl= mean(Probabilidadcl);
Desprool=std(Probabilidad);
Desprocl=std(Probabilidadcl);
CVprool=(Desprool*100)/mediaprool
CVprocl=(Desprocl*100)/mediaprocl
%------------------------------------------------------------------------------
%Grafica de Resultados de Cobertura del Algoritmo de PC
figuraPC;
%% Gr�fica de asignaci�n de recursos
  %  figure('color', [1 1 1],'Name','celda 1 UFR','NumberTitle','off')
  %  title('Asignaci�n de PRBs - UFR y Planificador')
  %  g_recursos(PF1up,3*nues,prb,rept);
save ValoresPTX.mat PTXUEol Ptransmision SINRol SINRcl;
FiguraPTX;
run 'celda_de_estudio'
%%
fopen('RP_RR.dat','wt');
dlmwrite('RP_RR.dat', tp_RR, 'delimiter', '\n', 'precision', '%.4f','-append');
fopen('RP_PF.dat','wt');
dlmwrite('RP_PF.dat', tp_PF, 'delimiter', '\n', 'precision', '%.4f','-append');
toc;
%% usuarios atendidos
if planificador ==4 || planificador ==5
[UA1,UA2,UA3,UA4]=us_atent(nues,MR1,MR2,MR3,MR4);
%delete(valores.dat);
end

