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

function graficas_planificador(p,col,celda,nue,prb,rept,throughput_c1,throughput_c2,throughput_c3,throughput_c4,R_C1,R_C2,R_C3,R_C4,SINR_c1,SINR_c2,SINR_c3,SINR_c4,SINR_T,PRX1,PRX2,PRX3,PRX4,Interferencia)

R_prom=zeros(1,rept); 
promedio=zeros(1,rept); 

throughput_sistema= (throughput_c1+throughput_c2+throughput_c3+throughput_c4);
promedio(1,:)=(sum(throughput_sistema))/rept; 

if(celda<=4)
    
switch celda
    
case 1
    
    %% Gráfica de potencia recibida
    figure('color', [1 1 1],'Name','Celda 1 UFR','NumberTitle','off')
    hist(PRX1(:))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de Potencia Recibida en Celda 1 UFR')
    xlabel('Potencia [dBm]')
    ylabel('Num. Ocurrencias')
    
    %% Gráficas de SINR
    figure('color', [1 1 1],'Name','Celda 1 UFR','NumberTitle','off')
    hist(reshape(SINR_c1,(nue*rept),1))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de SINR en Celda 1 UFR')
    xlabel('SINR [dB]')
    ylabel('Num. Ocurrencias')
    
    figure('color', [1 1 1],'Name','Celda 1 UFR','NumberTitle','off')
    h=cdfplot(SINR_c1(1:1:end));
    title ('CDF de SINR en Celda 1 UFR')
    xlabel('SINR [dB]')
    ylabel ('CDF')
    set (h,'color',col, 'Marker','o','LineStyle', '-')
    
    
    %% Gráfica de asignación de recursos
    figure('color', [1 1 1],'Name','celda 1 UFR','NumberTitle','off')
    title(['Asignación de PRBs - UFR y Planificador ' p])
    g_recursos(R_C1,nue,prb,rept);
    
    %% Gráficas de Throughput para planificadores RR
    figure('color', [1 1 1],'Name','Celda 1 UFR','NumberTitle','off')
    hist(throughput_c1,4)
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title(['Throughput con UFR y planificador ' p ' en Celda 1'])
    xlabel('Throughput [Mbps]')
    ylabel('Num. Ocurrencias')
       
    R_prom(1,:)=(sum(throughput_c1))/rept; %Throughput promedio 
    
    figure('color', [1 1 1],'Name','Celda 1 UFR','NumberTitle','off') 
    hold on  
    plot(throughput_c1,'color',col,'Marker','s','LineStyle', '-','linewidth',1.2)
    plot(R_prom,'color',col,'Marker','s','LineStyle', '-')
    title('Throghput Celda 1 UFR')
    xlabel('Subtrama')
    ylabel('Mbps')
    axis([1 rept 0 (max(throughput_c1)+5)])
    grid on
      
    figure('color', [1 1 1],'Name','Celda 1 UFR','NumberTitle','off')   
    hpf=cdfplot(throughput_c1(1:1:end));
    set (hpf,'color',col,'Marker','s','LineStyle', '-');
    title('CDF del Throghput Celda 1 UFR')
    xlabel('Mbps')
    ylabel('CDF')
   
    run 'analisis_ensayo'
        
 case 2
     
    %% Gráfica de potencia recibida
    figure('color', [1 1 1],'Name','Celda 2 UFR','NumberTitle','off')
    hist(PRX2(:))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de Potencia Recibida en Celda 2 UFR')
    xlabel('Potencia [dBm]')
    ylabel('Num. Ocurrencias')
    
    %% Gráficas de SINR
    figure('color', [1 1 1],'Name','Celda 2 UFR','NumberTitle','off')
    hist(reshape(SINR_c2,(nue*rept),1))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de SINR en Celda 2 UFR')
    xlabel('SINR [dB]')
    ylabel('Num. Ocurrencias')
    
    figure('color', [1 1 1],'Name','Celda 2 UFR','NumberTitle','off')
    h=cdfplot(SINR_c2(1:1:end));
    title ('CDF de SINR en Celda 2 UFR')
    xlabel('SINR [dB]')
    ylabel ('CDF')
    set (h,'color',col, 'Marker','o','LineStyle', '-')
        
    %% Gráfica de asignación de recursos
    figure('color', [1 1 1],'Name','Celda 2','NumberTitle','off')
    title(['Asignación de PRBs - Planificador ' p])
    g_recursos(R_C2,nue,prb,rept);

    %% Gráficas de Throughput para planificadores RR
    figure('color', [1 1 1],'Name','Celda 2 UFR','NumberTitle','off')
    hist(throughput_c2,4)
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title(['Throughput con UFR y planificador ' p ' en Celda 2'])
    xlabel('Throughput [Mbps]')
    ylabel('Num. Ocurrencias')
    
    R_prom(1,:)=(sum(throughput_c2))/rept; %Throughput promedio 
    
    figure('color', [1 1 1],'Name','Celda 2 UFR','NumberTitle','off') 
    hold on
    plot(throughput_c2,'color',col,'Marker','s','LineStyle', '-','linewidth',1.2)
    plot(R_prom,'color',col,'Marker','s','LineStyle', '-')
    axis([1 rept 0 (max(throughput_c2)+5)])
    grid on
    title('Throghput Celda 2 UFR')
    xlabel('Subtrama')
    ylabel('Mbps')
    
    figure('color', [1 1 1],'Name','Celda 2 UFR','NumberTitle','off')   
    hpf=cdfplot(throughput_c2(1:1:end));
    set (hpf,'color',col,'Marker','s','LineStyle', '-');
    title('Throghput Celda 2 UFR')
    xlabel('Mbps')
    ylabel('CDF')
    
    run 'analisis_ensayo'
 
 case 3
    
    %% Gráfica de potencia recibida
    figure('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')
    hist(PRX3(:))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de Potencia Recibida en Celda 3 UFR')
    xlabel('Potencia [dBm]')
    ylabel('Num. Ocurrencias')
    
    %% Gráficas de SINR
    figure('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')
    hist(reshape(SINR_c3,(nue*rept),1))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de SINR en Celda 3 UFR')
    xlabel('SINR [dB]')
    ylabel('Num. Ocurrencias')
    
    figure('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')
    h=cdfplot(SINR_c3(1:1:end));
    title ('CDF de SINR en Celda 3 UFR')
    xlabel('SINR [dB]')
    ylabel ('CDF')
    set (h,'color',col, 'Marker','o','LineStyle', '-')
    
    %% Gráfica de asignación de recursos
    figure('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')
    title(['Asignación de PRBs - UFR y Planificador ' p])
    g_recursos(R_C3,nue,prb,rept);
    
    %% Gráficas de Throughput para planificadores RR
    figure('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')
    hist(throughput_c3,4)
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title(['Throughput con UFR y planificador ' p ' en Celda 3'])
    xlabel('Throughput [Mbps]')
    ylabel('Num. Ocurrencias')
    
    R_prom(1,:)=(sum(throughput_c3))/rept; %Throughput promedio 
    
    figure ('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')   
    hold on
    plot(throughput_c3,'color',col,'Marker','s','LineStyle', '-','linewidth',1.2)
    plot(R_prom,'color',col,'Marker','s','LineStyle', '-')
    axis([1 rept 0 (max(throughput_c3)+5)])
    grid on
    title('Throghput Celda 3 UFR')
    xlabel('Subtrama')
    ylabel('Mbps')
      
    figure('color', [1 1 1],'Name','Celda 3 UFR','NumberTitle','off')   
    hpf=cdfplot(throughput_c3(1:1:end));
    set (hpf,'color',col,'Marker','s','LineStyle', '-');
    title('Throghput Celda 3 UFR')
    xlabel('Mbps')
    ylabel('CDF')
    
    run 'analisis_ensayo'
      
 case 4
   
    %% Gráfica de potencia recibida
    figure('color', [1 1 1],'Name','Celda 4 UFR','NumberTitle','off')
    hist(PRX4(:))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de Potencia Recibida en Celda 4 UFR')
    xlabel('Potencia [dBm]')
    ylabel('Num. Ocurrencias')
    
    %% Gráficas de SINR
    figure('color', [1 1 1],'Name','Celda 4 UFR','NumberTitle','off')
    hist(reshape(SINR_c4,(nue*rept),1))
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title('Histograma de SINR en Celda 4 UFR')
    xlabel('SINR [dB]')
    ylabel('Num. Ocurrencias')
    
    figure('color', [1 1 1],'Name','Celda 4 UFR','NumberTitle','off')
    h=cdfplot(SINR_c4(1:1:end));
    title ('CDF de SINR en Celda 4')
    xlabel('SINR [dB]')
    ylabel ('CDF')
    set (h,'color',col, 'Marker','o','LineStyle', '-')
    
    %% Gráfica de asignación de recursos
    figure('color', [1 1 1],'Name','Celda 4 UFR','NumberTitle','off')
    title(['Asignación de PRBs - UFR y Planificador ' p])
    g_recursos(R_C4,nue,prb,rept);
    
    %% Gráficas de Throughput para planificadores RR
    figure('color', [1 1 1],'Name','Celda 4 UFR','NumberTitle','off')
    hist(throughput_c4,4)
    h = findobj(gca,'Type','patch');
    set(h,'EdgeColor','w')
    title(['Throughput con UFR y planificador ' p ' en Celda 4'])
    xlabel('Throughput [Mbps]')
    ylabel('Num. Ocurrencias')
    
    R_prom(1,:)=(sum(throughput_c4))/rept; %Throughput promedio 
    
    figure('color', [1 1 1],'Name','Celda 4  UFR','NumberTitle','off')   
    hold on
    plot(throughput_c4,'color',col,'Marker','s','LineStyle', '-','linewidth',1.2)
    plot(R_prom,'color',col,'Marker','s','LineStyle', '-')
    axis([1 rept 0 (max(throughput_c4)+5)])
    grid on
    title('Throghput Celda 4 UFR')
    xlabel('Subtrama')
    ylabel('Mbps')
      
    figure ('color', [1 1 1],'Name','Celda 4 UFR','NumberTitle','off')   
    hpf=cdfplot(throughput_c4(1:1:end));
    set (hpf,'color',col,'Marker','s','LineStyle', '-');
    title('Throghput Celda 4 UFR')
    xlabel('Mbps')
    ylabel('CDF')
  
    run 'analisis_ensayo'
    
end

else
    
%% Gráficas de throughput total del sistema
    
figure('color', [1 1 1],'Name','Resultados Totales del Sistema UFR','NumberTitle','off') 
hist(SINR_T)
title('SINR Total del Sistema UFR')
xlabel('SINR [dB]')
ylabel('Num. Ocurrencias')

figure('color', [1 1 1],'Name','Resultados Totales del Sistema UFR','NumberTitle','off')
h=cdfplot(SINR_T(1:1:end));
title ('CDF de SINR Total del Sistema UFR')
xlabel('SINR [dB]')
ylabel ('CDF')
set (h,'color',[1 0 1], 'Marker','o','LineStyle', '-')

figure('color', [1 1 1],'Name','Resultados Totales del Sistema UFR','NumberTitle','off') 
hist(throughput_sistema,4)
h = findobj(gca,'Type','patch');
set(h,'EdgeColor','w')
title('Throughput Total de Sistema UFR')
xlabel('Throughput [Mbps]')
ylabel('Num. Ocurrencias')

figure('color', [1 1 1],'Name','Resultados Totales del Sistema UFR','NumberTitle','off')    
hold on
plot(throughput_sistema,'color',col,'Marker','v','LineStyle','-','linewidth',1.2)
plot(promedio,'color',col,'Marker','v','LineStyle','-')
axis([1 rept 0 (max(throughput_sistema)+20)])
grid on
title('Throughput Total del Sistema UFR')
xlabel('Subtrama')
ylabel('Throughput [Mbps]')
    
figure('color', [1 1 1],'Name','Resultados Totales del Sistema UFR','NumberTitle','off') 
hold on
hrr=cdfplot(throughput_sistema(1:1:end));
set(hrr,'color',col,'Marker','v','LineStyle','-');
title('CDF del Throughput Total del Sistema UFR')
xlabel('Throughput [Mbps]')
ylabel('CDF')    

figure('color', [1 1 1],'Name','Resultados Totales del Sistema UFR','NumberTitle','off')    
hold on
plot(throughput_c1,'gv-','linewidth',1.2)
plot(throughput_c2,'bs-','linewidth',1.2)
plot(throughput_c3,'rv-','linewidth',1.2)
plot(throughput_c4,'yv-','linewidth',1.2)
axis([1 rept 0 (max(throughput_c1)+10)])
grid on
title('Throughput Total de las Celdas del Sistema UFR')
xlabel('Subtrama')
ylabel('Throughput [Mbps]')

end
  