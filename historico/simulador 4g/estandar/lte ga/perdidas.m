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

function[Lc1, Lc2, Lc3, Lc4]=perdidas(p, nuec,d1, d2, d3, d4, fc)

Lc1=zeros(nuec,4);
Lc2=zeros(nuec,4);
Lc3=zeros(nuec,4);
Lc4=zeros(nuec,4);
Lo1=zeros(nuec,4);
Lo2=zeros(nuec,4);
Lo3=zeros(nuec,4);
Lo4=zeros(nuec,4);
Lrts=zeros(nuec,4);
kf=zeros(nuec,4);
Lmsd1=zeros(nuec,4);
Lmsd2=zeros(nuec,4);
Lmsd3=zeros(nuec,4);
Lmsd4=zeros(nuec,4);
Dhe=1.5;
switch p
    case 2 %Espacio libre
        for i=1:nuec
        for m1=1:4
        Lc1(i,m1)= 32.45+ 20*log10(d1(i,m1))+20*log10(fc);       
        Lc2(i,m1)= 32.45+ 20*log10(d2(i,m1))+20*log10(fc);
        Lc3(i,m1)= 32.45+ 20*log10(d3(i,m1))+20*log10(fc);
        Lc4(i,m1)= 32.45+ 20*log10(d4(i,m1))+20*log10(fc);
        end
        end
   
    case 3 %COST 231 macro urbano
         cm=3;% Factor de correccion para centros metropolitanos
         Dhb=32;% valor de acuerdo a TR25.996
         
         for i=1:nuec
         for m1=1:4
             a=(1.1*log10(fc- 0.7))*Dhe -(1.56*log10(fc)-0.8);
         Lc1(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d1(i,m1))+ cm;
         Lc2(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d2(i,m1))+ cm;
         Lc3(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d3(i,m1))+ cm;
         Lc4(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d4(i,m1))+ cm;
         end
         end
    case 4 %COST 231 micro urbano
         %Valores de acuerdo a TR125.996
         Dhb=12.5; % altura de la antena del eNB en m.
         Dhroof=12;% altura del edificio en m
         phi=30;
         w=25; % distancia en m.
         b=50; % separacion entre edificios.
         %PL=Lo (dB)+Lrts (dB)+Lmsd (dB)
         for i=1:nuec
         for m1=1:4
         Lo1(i,m1)=32.4 + 20*log10(d1(i,m1)) + 20*log10(fc); %free space loss
         Lo2(i,m1)=32.4 + 20*log10(d2(i,m1)) + 20*log10(fc); 
         Lo3(i,m1)=32.4 + 20*log10(d3(i,m1)) + 20*log10(fc); 
         Lo4(i,m1)=32.4 + 20*log10(d4(i,m1)) + 20*log10(fc); 
         Lori = -10 + 0.354*phi; % Valor de L.ori para ((0 <= phi) & (phi < 35))
         Lrts(i,1)=-16.9 - 10*log10(w) + 10*log10(fc) + 20*log10(Dhe) + Lori ; %roof-top-to-street diffracton and scatter loss
         %L_msd = Lbsh + ka + kd*log10(d) + kf*log10(freq) - 9*log10(b); %multiple screen diffraction loss
         delta_hbase=(Dhb-Dhroof);
         Lbsh= -18*log10(1 + delta_hbase);% Perdida por la separacion entre edificios. Valor para Dhb>Dhroof.
         ka=54; % Valor de Ka para Dhb>Dhroof.
         kd=18; % Valor de Kb para Dhb>Dhroof.
         kf(i,1)= -4 + 1.5*((fc/925 )- 1); % Se considera un centro metropolitano
         Lmsd1(i,m1) = Lbsh + ka + kd*log10(d1(i,m1)) + kf(i,1)*log10(fc) - 9*log10(b);
         Lmsd2(i,m1) = Lbsh + ka + kd*log10(d2(i,m1)) + kf(i,1)*log10(fc) - 9*log10(b);
         Lmsd3(i,m1) = Lbsh + ka + kd*log10(d3(i,m1)) + kf(i,1)*log10(fc) - 9*log10(b);
         Lmsd4(i,m1) = Lbsh + ka + kd*log10(d4(i,m1)) + kf(i,1)*log10(fc) - 9*log10(b);                  
         Lc1(i,m1)=Lo1(i,m1)+Lrts(i,1)+Lmsd1(i,m1);
         Lc2(i,m1)=Lo2(i,m1)+Lrts(i,1)+Lmsd2(i,m1);
         Lc3(i,m1)=Lo3(i,m1)+Lrts(i,1)+Lmsd3(i,m1);
         Lc4(i,m1)=Lo4(i,m1)+Lrts(i,1)+Lmsd4(i,m1);
         end
         end

    case 5 %COST 231 suburban macro
         cm=0;% Factor de correccion para areas suburbanas
         Dhb=32;% valor de acuerdo a TR 125.996
        
         
         for i=1:nuec
         for m1=1:4
         a=(1.1*log10(fc - 0.7))*Dhe -(1.56*log10(fc)-0.8);
         Lc1(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d1(i,m1)) + cm;
         Lc2(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d2(i,m1)) + cm;
         Lc3(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d3(i,m1)) + cm;
         Lc4(i,m1)=46.3 + 33.9*log10(fc) - 13.82*log10(Dhb) - a + (44.9 - 6.55*log10(Dhb))*log10(d4(i,m1)) + cm;
         end
         end
    case 6 %TS 36.942 urbano
        Dhb=15;
        for i=1:nuec
        for m1=1:4
        Lc1(i,m1)= 40*(1-(4*10^-3)*Dhb)*log10(d1(i,m1))-18*log10(Dhb)+21*log10(fc)+80; %Calculo de perdidas con modelo Macro cell propagation–Urban Area TS 36.942dB
        Lc2(i,m1)= 40*(1-(4*10^-3)*Dhb)*log10(d2(i,m1))-18*log10(Dhb)+21*log10(fc)+80;
        Lc3(i,m1)= 40*(1-(4*10^-3)*Dhb)*log10(d3(i,m1))-18*log10(Dhb)+21*log10(fc)+80;
        Lc4(i,m1)= 40*(1-(4*10^-3)*Dhb)*log10(d4(i,m1))-18*log10(Dhb)+21*log10(fc)+80;
        end
        end
    case 7 %TS 36.942 suburbano'
       Dhb=15;
       for i=1:nuec
       for m1=1:4
       Lc1(i,m1)= 69.55+26.16*log10(fc)-13.82*log10(Dhb)+(44.9-6.55*log10(Dhb))*log10(d1(i,m1))-4.78*(log10((fc).^2))+18.33*log10(fc)-40.99; % Calculo con modelo Macro cell propagation Suburban Area TS 36.942 dB
       Lc2(i,m1)= 69.55+26.16*log10(fc)-13.82*log10(Dhb)+(44.9-6.55*log10(Dhb))*log10(d2(i,m1))-4.78*(log10((fc).^2))+18.33*log10(fc)-40.99;
       Lc3(i,m1)= 69.55+26.16*log10(fc)-13.82*log10(Dhb)+(44.9-6.55*log10(Dhb))*log10(d3(i,m1))-4.78*(log10((fc).^2))+18.33*log10(fc)-40.99;
       Lc4(i,m1)= 69.55+26.16*log10(fc)-13.82*log10(Dhb)+(44.9-6.55*log10(Dhb))*log10(d4(i,m1))-4.78*(log10((fc).^2))+18.33*log10(fc)-40.99;
       end
      end
end