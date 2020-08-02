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

function varargout = analisis_ensayo(varargin)
% ANALISIS_ENSAYO MATLAB code for analisis_ensayo.fig
%      ANALISIS_ENSAYO, by itself, creates a new ANALISIS_ENSAYO or raises the existing
%      singleton*.
%
%      H = ANALISIS_ENSAYO returns the handle to a new ANALISIS_ENSAYO or the handle to
%      the existing singleton*.
%
%      ANALISIS_ENSAYO('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ANALISIS_ENSAYO.M with the given input arguments.
%
%      ANALISIS_ENSAYO('Property','Value',...) creates a new ANALISIS_ENSAYO or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before analisis_ensayo_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to analisis_ensayo_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help analisis_ensayo

% Last Modified by GUIDE v2.5 12-Mar-2015 12:19:13

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @analisis_ensayo_OpeningFcn, ...
                   'gui_OutputFcn',  @analisis_ensayo_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before analisis_ensayo is made visible.
function analisis_ensayo_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to analisis_ensayo (see VARARGIN)

% Choose default command line output for analisis_ensayo
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

movegui('center');

%Se selecciona el UE de la celda de estudio 
global nues;
c={zeros(1,3*nues)};

for i=1:3*nues
    c(i,1)={['UE ' num2str(i)]};
end
 cadena=['Seleccionar Usuario'; c];
set(handles.popupmenu1,'String',cadena); 

% UIWAIT makes analisis_ensayo wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = analisis_ensayo_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1


% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

c=[1 0.3 0.5 0 0.2 0.8 1 0.1 0.7 0.4 1 0.3 0.5 1 0.5 0.8 0.7 0.9 0.2 0.4 1 0.5 0.8 0.6 0.5 0.4 0.8 1 1 0.2 0.8 0.4 0.8 0.4 0.4 0.1 0.6 0.8 0.9 0.5 1 0.2 0.8 1 0.9 0.5 0.7 0.3 0.6 0.5;
   1 0.6 0.3 0.9 0.2 1 0.3 0.7 0.3 1 0.2 0.3 0.8 0.4 0.5 0.6 1 0.2 0.9 0.1 0.5 0.7 0.8 0.5 0.4 0.3 0.6 0.3 0.8 0.2 0.4 0 1 0.7 0.8 0.8 0.9 0.3 0.2 0.4 0.5 0.1 0.4 0.7 0.9 0.3 0.6 0.3 0.2 0.5;
   0 1 0 0 0.2 1 0.2 0.7 0.5 0.8 0.8 0.9 0.6 1 0.4 0.5 0.1 0.4 0.7 0.9 0.3 0.6 0.3 0.2 0.5 0.5 1 0.5 0.8 0.7 0.9 0.2 0.4 1 0.5 0.8 0.6 0.5 0.9 0.4 0.3 0.8 0.4 0.1 0.6 0.8 0.9 0.3 0.2 1];

col=[c flipud(c)];

%%

global planificador
global RR1 RR2 RR3 RR4
global PF1 PF2 PF3 PF4
global MR1 MR2 MR3 MR4
global minSINR
global SINR_c1 SINR_c2 SINR_c3 SINR_c4
global celda
global nues rept

global throughput_c1_RR throughput_c2_RR throughput_c3_RR throughput_c4_RR
global throughput_c1_PF throughput_c2_PF throughput_c3_PF throughput_c4_PF
global throughput_c1_MR throughput_c2_MR throughput_c3_MR throughput_c4_MR

ue=get(handles.popupmenu1,'Value')-1;



a=size(MR1);
lvl=zeros(1, a(1,2));
lvl(1,:)=minSINR;

switch celda

case 1
%%
         
   if(ue>0 && planificador==2) % Estrategia de planificación RR
   
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(RR1(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c1(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c1_RR(ue,:)))/rept; %Throughput promedio celda 1 con planificador RR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c1_RR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'color',[0 0.8 0],'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
 
 
%%
else if(ue>0 && planificador==3) % Estrategia de planificación PF
   
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off')
   con=(PF1(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c1(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama') 
   ylabel ('SRBs asignados / SINR [dB]')
      
   prom=(sum(throughput_c1_PF(ue,:)))/rept; %Throughput promedio celda 1 con planificador PF
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c1_PF(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
      
%%
else if(ue>0 && planificador==4) % Estrategia de planificación MR
   
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(MR1(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c1(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c1_MR(ue,:)))/rept; %Throughput promedio celda 1 con planificador MR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c1_MR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'r--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
   
    
%%
else if(ue>0 && planificador==5) % Estrategias de planificación RR,PF y MR
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off') 
   PRM=zeros(3*nues,rept);
   con1=[RR1(ue,:)' PRM(ue,:)' PRM(ue,:)'];
   con2=[PRM(ue,:)' PF1(ue,:)' PRM(ue,:)'];
   con3=[PRM(ue,:)' PRM(ue,:)' MR1(ue,:)'];
   
   hold on;
   bar(con1,'g');
   hold on;
   bar(con2,'b');
   hold on;
   bar(con3,'r');
   hold on;
   plot((SINR_c1(ue,:)),'k--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda)])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   p1=(sum(throughput_c1_RR(ue,:)))/rept; %Throughput promedio celda 1 con planificador RR
   l1=zeros(1, rept);
   l1(1,:)=p1;
   p2=(sum(throughput_c1_PF(ue,:)))/rept; %Throughput promedio celda 1 con planificador PF
   l2=zeros(1, rept);
   l2(1,:)=p2;
   p3=(sum(throughput_c1_MR(ue,:)))/rept; %Throughput promedio celda 1 con planificador MR
   l3=zeros(1, rept);
   l3(1,:)=p3;
   
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   hold on;
   plot((throughput_c1_RR(ue,:)),'color',[0 0.8 0],'LineStyle','--','Marker','o')
   plot((throughput_c1_PF(ue,:)),'--','Marker','o')
   plot((throughput_c1_MR(ue,:)),'r--','Marker','o')
   
   plot(l1,'color',[0 0.8 0],'LineStyle','-','Marker','*')
   plot(l2,'-','Marker','*')
   plot(l3,'r-','Marker','*')
   grid on; 
   legend(['T. del UE ' int2str(ue) ', Planificador RR'],['T. del UE ' int2str(ue) ', Planificador PF'],['T. del UE ' int2str(ue) ', Planificador MR'],['T. Promedio del UE ' int2str(ue) ', Planificador RR'],['T. Promedio del UE ' int2str(ue) ', Planificador PF'],['T. Promedio del UE ' int2str(ue) ', Planificador MR'])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
   
   
         
else
     errordlg('Debe elegir un usuario','Error')
   
    end
    end
    end
    end
%%
case 2
    %%

   if(ue>0 && planificador==2) % Estrategia de planificación RR
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(RR2(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c2(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
 
   prom=(sum(throughput_c2_RR(ue,:)))/rept; %Throughput promedio celda 2 con planificador RR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c2_RR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'color',[0 0.8 0],'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
 
%%
else if(ue>0 && planificador==3) % Estrategia de planificación PF
   
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off')
   con=(PF2(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c2(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c2_PF(ue,:)))/rept; %Throughput promedio celda 2 con planificador PF
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c2_PF(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
      
%%
else if(ue>0 && planificador==4) % Estrategia de planificación MR
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(MR2(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c2(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c2_MR(ue,:)))/rept; %Throughput promedio celda 2 con planificador MR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c2_MR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'r--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
    
%%
else if(ue>0 && planificador==5) % Estrategias de planificación RR,PF y MR
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off') 
   PRM=zeros(3*nues,rept);
   con1=[RR2(ue,:)' PRM(ue,:)' PRM(ue,:)'];
   con2=[PRM(ue,:)' PF2(ue,:)' PRM(ue,:)'];
   con3=[PRM(ue,:)' PRM(ue,:)' MR2(ue,:)'];
   
   hold on;
   bar(con1,'g');
   hold on;
   bar(con2,'b');
   hold on;
   bar(con3,'r');
   hold on;
   plot((SINR_c2(ue,:)), 'k--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda)])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   p1=(sum(throughput_c2_RR(ue,:)))/rept; %Throughput promedio celda 2 con planificador RR
   l1=zeros(1, rept);
   l1(1,:)=p1;
   p2=(sum(throughput_c2_PF(ue,:)))/rept; %Throughput promedio celda 2 con planificador PF
   l2=zeros(1, rept);
   l2(1,:)=p2;
   p3=(sum(throughput_c2_MR(ue,:)))/rept; %Throughput promedio celda 2 con planificador MR
   l3=zeros(1, rept);
   l3(1,:)=p3;
   
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   hold on;
   plot((throughput_c2_RR(ue,:)),'color',[0 0.8 0],'LineStyle','--','Marker','o')
   plot((throughput_c2_PF(ue,:)),'--','Marker','o')
   plot((throughput_c2_MR(ue,:)),'r--','Marker','o')
   plot(l1,'color',[0 0.8 0],'LineStyle','-','Marker','*')
   plot(l2,'-','Marker','*')
   plot(l3,'r-','Marker','*')
   grid on; 
   legend(['T. del UE ' int2str(ue) ', Planificador RR'],['T. del UE ' int2str(ue) ', Planificador PF'],['T. del UE ' int2str(ue) ', Planificador MR'],['T. Promedio del UE ' int2str(ue) ', Planificador RR'],['T. Promedio del UE ' int2str(ue) ', Planificador PF'],['T. Promedio del UE ' int2str(ue) ', Planificador MR'])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
         
else
     errordlg('Debe elegir un usuario','Error')
   
    end
    end
    end
   end
    
case 3
    %%

   if(ue>0 && planificador==2) % Estrategia de planificación RR
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(RR3(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c3(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c3_RR(ue,:)))/rept; %Throughput promedio celda 3 con planificador RR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c3_RR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'color',[0 0.8 0],'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
 
 
%%
else if(ue>0 && planificador==3) % Estrategia de planificación PF
   
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off')
   con=(PF3(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c3(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c3_PF(ue,:)))/rept; %Throughput promedio celda 1 con planificador PF
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c3_PF(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
      
%%
else if(ue>0 && planificador==4) % Estrategia de planificación MR
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(MR3(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c3(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c3_MR(ue,:)))/rept; %Throughput promedio celda 1 con planificador MR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c3_MR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'r--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
    
%%
else if(ue>0 && planificador==5) % Estrategias de planificación RR,PF y MR
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off') 
   PRM=zeros(3*nues,rept);
   con1=[RR3(ue,:)' PRM(ue,:)' PRM(ue,:)'];
   con2=[PRM(ue,:)' PF3(ue,:)' PRM(ue,:)'];
   con3=[PRM(ue,:)' PRM(ue,:)' MR3(ue,:)'];
   
   hold on;
   bar(con1,'g');
   hold on;
   bar(con2,'b');
   hold on;
   bar(con3,'r');
   hold on;
   plot((SINR_c3(ue,:)), 'k--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda)])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
    
   p1=(sum(throughput_c3_RR(ue,:)))/rept; %Throughput promedio celda 3 con planificador RR
   l1=zeros(1, rept);
   l1(1,:)=p1;
   p2=(sum(throughput_c3_PF(ue,:)))/rept; %Throughput promedio celda 3 con planificador PF
   l2=zeros(1, rept);
   l2(1,:)=p2;
   p3=(sum(throughput_c3_MR(ue,:)))/rept; %Throughput promedio celda 3 con planificador MR
   l3=zeros(1, rept);
   l3(1,:)=p3;
   
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   hold on;
   plot((throughput_c3_RR(ue,:)),'color',[0 0.8 0],'LineStyle','--','Marker','o')
   plot((throughput_c3_PF(ue,:)),'--','Marker','o')
   plot((throughput_c3_MR(ue,:)),'r--','Marker','o')
   plot(l1,'color',[0 0.8 0],'LineStyle','-','Marker','*')
   plot(l2,'-','Marker','*')
   plot(l3,'r-','Marker','*')
   grid on; 
   legend(['T. del UE ' int2str(ue) ', Planificador RR'],['T. del UE ' int2str(ue) ', Planificador PF'],['T. del UE ' int2str(ue) ', Planificador MR'],['T. Promedio del UE ' int2str(ue) ', Planificador RR'],['T. Promedio del UE ' int2str(ue) ', Planificador PF'],['T. Promedio del UE ' int2str(ue) ', Planificador MR'])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
         
else
     errordlg('Debe elegir un usuario','Error')
   
    end
    end
    end
   end
    
case 4
    %%

   if(ue>0 && planificador==2) % Estrategia de planificación RR
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(RR4(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c4(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c4_RR(ue,:)))/rept; %Throughput promedio celda 4 con planificador RR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c4_RR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'color',[0 0.8 0],'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador RR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
 
 
%%
else if(ue>0 && planificador==3) % Estrategia de planificación PF
   
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off')
   con=(PF4(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c4(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c4_PF(ue,:)))/rept; %Throughput promedio celda 1 con planificador PF
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c4_PF(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'LineStyle','--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador PF'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
      
%%
else if(ue>0 && planificador==4) % Estrategia de planificación MR
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   con=(MR4(ue,:)');
   bar(con,'FaceColor',[col(1,ue) col(2,ue) col(3,ue)]);
   grid on;
   hold on;
   plot((SINR_c4(ue,:)),'LineStyle', '--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
   prom=(sum(throughput_c4_MR(ue,:)))/rept; %Throughput promedio celda 1 con planificador MR
   lv=zeros(1, rept);
   lv(1,:)=prom;
      
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   plot((throughput_c4_MR(ue,:)),'k--','Marker','o','linewidth',2)
   grid on; 
   hold on;
   plot(lv,'r--','Marker','o','linewidth',2)
   legend(['T. del UE ' int2str(ue) ' en cada subtrama'],['T. Promedio del UE ' int2str(ue)])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ' - Planificador MR'])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
    
%%
else if(ue>0 && planificador==5) % Estrategias de planificación RR,PF y MR
   figure('color', [1 1 1],'Name',['PRBs Asignados y SINR del UE ' int2str(ue)],'NumberTitle','off') 
   PRM=zeros(3*nues,rept);
   con1=[RR4(ue,:)' PRM(ue,:)' PRM(ue,:)'];
   con2=[PRM(ue,:)' PF4(ue,:)' PRM(ue,:)'];
   con3=[PRM(ue,:)' PRM(ue,:)' MR4(ue,:)'];
   
   hold on;
   bar(con1,'g');
   hold on;
   bar(con2,'b');
   hold on;
   bar(con3,'r');
   hold on;
   plot((SINR_c4(ue,:)),'k--','Marker','o','linewidth',2)
   plot(lvl,'r--','Marker','o')
   grid on;
   title (['SRBs y SINR del UE ' num2str(ue) ' en Celda ' num2str(celda)])
   xlabel('Subtrama')
   ylabel ('SRBs asignados / SINR [dB]')
   
    
   p1=(sum(throughput_c4_RR(ue,:)))/rept; %Throughput promedio celda 4 con planificador RR
   l1=zeros(1, rept);
   l1(1,:)=p1;
   p2=(sum(throughput_c4_PF(ue,:)))/rept; %Throughput promedio celda 4 con planificador PF
   l2=zeros(1, rept);
   l2(1,:)=p2;
   p3=(sum(throughput_c4_MR(ue,:)))/rept; %Throughput promedio celda 4 con planificador MR
   l3=zeros(1, rept);
   l3(1,:)=p3;
   
   figure('color', [1 1 1],'Name',['UE ' int2str(ue)],'NumberTitle','off')
   hold on;
   plot((throughput_c4_RR(ue,:)),'color',[0 0.8 0],'LineStyle','--','Marker','o')
   plot((throughput_c4_PF(ue,:)),'--','Marker','o')
   plot((throughput_c4_MR(ue,:)),'r--','Marker','o')
   plot(l1,'color',[0 0.8 0],'LineStyle','-','Marker','*')
   plot(l2,'-','Marker','*')
   plot(l3,'r-','Marker','*')
   grid on; 
   legend(['T. del UE ' int2str(ue) ', Planificador RR'],['T. del UE ' int2str(ue) ', Planificador PF'],['T. del UE ' int2str(ue) ', Planificador MR'],['T. Promedio del UE ' int2str(ue) ', Planificador RR'],['T. Promedio del UE ' int2str(ue) ', Planificador PF'],['T. Promedio del UE ' int2str(ue) ', Planificador MR'])
   title ([' Throughput del UE ' num2str(ue) ' en Celda ' num2str(celda) ])
   xlabel('Subtrama')
   ylabel ('Throughput [Mbps]')
         
else
     errordlg('Debe elegir un usuario','Error')
   
    end
    end
    end
   end
    
end%% switch
