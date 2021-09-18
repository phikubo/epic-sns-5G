function[prx, pdl, pdr]=pot_celdaup(m, nuec, Lc, Ptx)
%% Calculo de las potencias en cada celda 
%Autor Angela Julieth Moreno Delgado
%Versión 0.4, 2016
% % Celda 
 GeNB = 18;
 prx= Ptx(:,m) + GeNB -Lc(:,m);
 % Potencia incluyendo el desvanecimiento lento y rapido
 N= 4*randn(nuec,1);
 pdl= N + prx;    % desvanecimiento lento
 prx_des_lv= 10.^(pdl./10);
 rel_vol= sqrt(prx_des_lv);
 b= rel_vol/sqrt(pi./2);
 prx_des_rl_v= raylrnd(b);
 pdr=20*log10(prx_des_rl_v);
 
 %Evaluar si Ptx = 0 para poner prx =0
 for i=1:nuec
     if(Ptx(i,m)==0)
         prx(i,1)=0;
         pdl(i,1)=0;
         pdr(i,1)=0;
     end
 end
end