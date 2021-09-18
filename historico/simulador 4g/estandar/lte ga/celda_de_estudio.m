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

function varargout = celda_de_estudio(varargin)
% CELDA_DE_ESTUDIO MATLAB code for celda_de_estudio.fig
%      CELDA_DE_ESTUDIO, by itself, creates a new CELDA_DE_ESTUDIO or raises the existing
%      singleton*.
%
%      H = CELDA_DE_ESTUDIO returns the handle to a new CELDA_DE_ESTUDIO or the handle to
%      the existing singleton*.
%
%      CELDA_DE_ESTUDIO('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CELDA_DE_ESTUDIO.M with the given input arguments.
%
%      CELDA_DE_ESTUDIO('Property','Value',...) creates a new CELDA_DE_ESTUDIO or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before celda_de_estudio_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to celda_de_estudio_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help celda_de_estudio

% Last Modified by GUIDE v2.5 26-Oct-2016 09:28:33

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @celda_de_estudio_OpeningFcn, ...
                   'gui_OutputFcn',  @celda_de_estudio_OutputFcn, ...
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


% --- Executes just before celda_de_estudio is made visible.
function celda_de_estudio_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to celda_de_estudio (see VARARGIN)

% Choose default command line output for celda_de_estudio
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

movegui('center');
% UIWAIT makes celda_de_estudio wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = celda_de_estudio_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on selection change in pop1.
function pop1_Callback(hObject, eventdata, handles)
% hObject    handle to pop1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns pop1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from pop1
 
% --- Executes during object creation, after setting all properties.
function pop1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to pop1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in DL.
function DL_Callback(hObject, eventdata, handles)
% hObject    handle to DL (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global celda
celda =get(handles.pop1,'Value')-1;
global planificador
global nues prb rept

global RR1 RR2 RR3 RR4
global PF1 PF2 PF3 PF4
global MR1 MR2 MR3 MR4

global throughput_c1_RR throughput_c2_RR throughput_c3_RR throughput_c4_RR
global throughput_c1_PF throughput_c2_PF throughput_c3_PF throughput_c4_PF
global throughput_c1_MR throughput_c2_MR throughput_c3_MR throughput_c4_MR

global SINR_c1 SINR_c2 SINR_c3 SINR_c4 SINR_T
global PRX1 PRX2 PRX3 PRX4
global Interferencia

if celda ==0
        msgbox('No ha Seleccionado una opcion','seleccione');
else
switch planificador
case 2 %%Estrategia de planificación Round Robin(RR)
graficas_planificador('RR',[0 0.8 0],celda,3*nues,prb,rept,sum(throughput_c1_RR),sum(throughput_c2_RR),sum(throughput_c3_RR),sum(throughput_c4_RR),RR1,RR2,RR3,RR4,SINR_c1,SINR_c2,SINR_c3,SINR_c4,SINR_T,PRX1,PRX2,PRX3,PRX4, Interferencia);

case 3 % Estrategia de planificación PF
graficas_planificador('PF','b',celda,3*nues,prb,rept,sum(throughput_c1_PF),sum(throughput_c2_PF),sum(throughput_c3_PF),sum(throughput_c4_PF),PF1,PF2,PF3,PF4,SINR_c1,SINR_c2,SINR_c3,SINR_c4,SINR_T,PRX1,PRX2,PRX3,PRX4, Interferencia);
   
case 4 % Estrategia de planificación MR
graficas_planificador('MR','r',celda,3*nues,prb,rept,sum(throughput_c1_MR),sum(throughput_c2_MR),sum(throughput_c3_MR),sum(throughput_c4_MR),MR1,MR2,MR3,MR4,SINR_c1,SINR_c2,SINR_c3,SINR_c4,SINR_T,PRX1,PRX2,PRX3,PRX4, Interferencia);

case 5 %%Estrategias de plnificación RR,PF y MR simultáneamente
planif_simult('RR','PF','MR',celda,3*nues,prb,rept,sum(throughput_c1_RR),sum(throughput_c2_RR),sum(throughput_c3_RR),sum(throughput_c4_RR),RR1,RR2,RR3,RR4,sum(throughput_c1_PF),sum(throughput_c2_PF),sum(throughput_c3_PF),sum(throughput_c4_PF),PF1,PF2,PF3,PF4,sum(throughput_c1_MR),sum(throughput_c2_MR),sum(throughput_c3_MR),sum(throughput_c4_MR),MR1,MR2,MR3,MR4,SINR_c1,SINR_c2,SINR_c3,SINR_c4,SINR_T,PRX1,PRX2,PRX3,PRX4,Interferencia)
end
end

% --- Executes on button press in UL.
function UL_Callback(hObject, eventdata, handles)
% hObject    handle to UL (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global celda
celda =get(handles.pop1,'Value')-1;
if celda == 5
    msgbox('Esta opción no esta habilitada para el UPLINK','No habilitado');
elseif celda ==0
    msgbox('No a Seleccionado una Opcion','Seleccione');
else
  Resultados_Uplink;  
end

