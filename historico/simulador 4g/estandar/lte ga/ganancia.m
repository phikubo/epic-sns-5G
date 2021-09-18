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

% Asignación de la ganancia de la antena

function[Gc1, Gc2, Gc3, Gc4]=ganancia(t, nuec, theta1, theta2, theta3, theta4)

Gc1=zeros(nuec,4);
Gc2=zeros(nuec,4);
Gc3=zeros(nuec,4);
Gc4=zeros(nuec,4);

switch t  % Segun el tipo de antena.

case 2  % Katherein 742215
    
        MXX=dlmread('Katherein_742215_Mod.prn');
        theta_hor=MXX(:,1);
        GANANCIA_HOR_N=(MXX(:,2)-5)-max(MXX(:,2));
                
        for a=1:nuec
               for x=1:4
                     for i=1:360
               if floor(theta1(a,x))==theta_hor(i,1);
               Gc1(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta2(a,x))==theta_hor(i,1);
               Gc2(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta3(a,x))==theta_hor(i,1);
               Gc3(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta4(a,x))==theta_hor(i,1);
               Gc4(a,x)=GANANCIA_HOR_N(i,1);
               end
                             
                     end
               end
        end
            
case 3   % Katherein 80010681
       
        MXX=dlmread('katherein_80010681_Mod.prn');
        theta_hor=MXX(:,1);
        GANANCIA_HOR_N=(MXX(:,2)-10)-max(MXX(:,2));
    
        for a=1:nuec
               for x=1:4
                     for i=1:360
               if floor(theta1(a,x))==theta_hor(i,1);
               Gc1(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta2(a,x))==theta_hor(i,1);
               Gc2(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta3(a,x))==theta_hor(i,1);
               Gc3(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta4(a,x))==theta_hor(i,1);
               Gc4(a,x)=GANANCIA_HOR_N(i,1);
               end
                             
                     end
               end
        end

case 4 %TR 36.942  
    
        MXX=dlmread('TR36942_Mod.prn');
        theta_hor=MXX(:,1);
        GANANCIA_HOR_N=MXX(:,2);
              
        for a=1:nuec
               for x=1:4
                     for i=1:360
               if floor(theta1(a,x))==theta_hor(i,1);
               Gc1(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta2(a,x))==theta_hor(i,1);
               Gc2(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta3(a,x))==theta_hor(i,1);
               Gc3(a,x)=GANANCIA_HOR_N(i,1);
               end
               if floor(theta4(a,x))==theta_hor(i,1);
               Gc4(a,x)=GANANCIA_HOR_N(i,1);
               end
                             
                     end
               end
        end
    
%         gan_antena=5;
%     
%         Gc1_n= -min((12*(theta1./65).^2),20);
%         Gc1=Gc1_n+gan_antena;
%         Gc2_n= -min((12*(theta2./65).^2),20);
%         Gc2=Gc2_n+gan_antena;
%         Gc3_n= -min((12*(theta3./65).^2),20);
%         Gc3=Gc3_n+gan_antena;
%         Gc4_n= -min((12*(theta4./65).^2),20);
%         Gc4=Gc4_n+gan_antena;
end
    
end
