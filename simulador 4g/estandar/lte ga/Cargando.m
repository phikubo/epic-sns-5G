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

function varargout = Cargando(varargin)
% CARGANDO MATLAB code for Cargando.fig
%      CARGANDO, by itself, creates a new CARGANDO or raises the existing
%      singleton*.
%
%      H = CARGANDO returns the handle to a new CARGANDO or the handle to
%      the existing singleton*.
%
%      CARGANDO('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CARGANDO.M with the given input arguments.
%
%      CARGANDO('Property','Value',...) creates a new CARGANDO or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Cargando_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Cargando_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Cargando

% Last Modified by GUIDE v2.5 02-Mar-2015 18:55:02

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Cargando_OpeningFcn, ...
                   'gui_OutputFcn',  @Cargando_OutputFcn, ...
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


% --- Executes just before Cargando is made visible.
function Cargando_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Cargando (see VARARGIN)

% Choose default command line output for Cargando
handles.output = hObject;

global estudio
global k sector carg
global rept NumSim car
global ob
switch estudio

case 1
    
if (sector==0)
je = javax.swing.JEditorPane('text/html', '<html><img src="file:\C:\Users\Equipo\Desktop\simulador\cargando.gif"></html>');
[hj, hc] =  javacomponent(je,[]);
set(hc, 'pos', [90,85,250,110])
end

case 2

if (NumSim==0)
    %Gif Cargando de Matlab 
try
    % R2010a and newer
    iconsClassName = 'com.mathworks.widgets.BusyAffordance$AffordanceSize';
    iconsSizeEnums = javaMethod('values',iconsClassName);
    SIZE_32x32 = iconsSizeEnums(2);  % (1) = 16x16,  (2) = 32x32
    jObj = com.mathworks.widgets.BusyAffordance(SIZE_32x32, 'Cargando...');  % icon, label
catch
    % R2009b and earlier
    redColor   = java.awt.Color(1,0,0);
    blackColor = java.awt.Color(0,0,0);
    jObj = com.mathworks.widgets.BusyAffordance(redColor, blackColor);
end
jObj.setPaintsWhenStopped(true);  % default = false
jObj.useWhiteDots(false);         % default = false (true is good for dark backgrounds)
javacomponent(jObj.getComponent, [100,90,90,90], gcf);
jObj.start;
ob = jObj;
end
end

% Update handles structure
guidata(hObject, handles);
movegui('center');

switch estudio

case 1
    
if k==1
    carg=num2str(floor((100/12)*sector));
elseif k==2
    carg=num2str(floor((100/12)*(sector+3)));
elseif k==3
    carg=num2str(floor((100/12)*(sector+6)));
elseif k==4
    carg=num2str(floor((100/12)*(sector+9)));
end
set(handles.text1,'String',[carg '%'])
set(handles.text2,'String','Obteniendo Resultados de Cobertura.')
    
case 2
    
car=num2str(floor(100/rept)*NumSim);
set(handles.text1,'String',[car '%'])
set(handles.text2,'String','Obteniendo Resultados de Capacidad.')
if (NumSim ==10)
    ob.stop;
    ob.setBusyText('Listo!');
end
end

% UIWAIT makes Cargando wait for user response (see UIRESUME)
% uiwait(handles.figure1);
% --- Outputs from this function are returned to the command line.
function varargout = Cargando_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
%Para Cerrar interfaz de Cargando
global estudio car carg
switch estudio
case 1
if (str2double(carg)==100)
    close (gcf)  
end
    
case 2
if (str2double(car)==100)
     close (gcf)  
end
end
% --- Executes during object creation, after setting all properties.
function text1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to text1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
