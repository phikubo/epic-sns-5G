% Simulador Básico a Nivel de Sistema para LTE con Algoritmos de Control de Potencia.
% Licencia academica, no comercial.
% Descripción: Interfaz grafica que muestra los resultados de cobertura en uplink de
% los algoritmos de control de potencia implementados en el sistema LTE.
% Autor: Angela Julieth Moreno Delgado.
% Grupo de Radio e Inalambricas GRIAL
% Universidad del Cauca
% 2016-2017
function varargout = figuraPC(varargin)
% FIGURAPC MATLAB code for figuraPC.fig
%      FIGURAPC, by itself, creates a new FIGURAPC or raises the existing
%      singleton*.
%
%      H = FIGURAPC returns the handle to a new FIGURAPC or the handle to
%      the existing singleton*.
%
%      FIGURAPC('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FIGURAPC.M with the given input arguments.
%
%      FIGURAPC('Property','Value',...) creates a new FIGURAPC or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before figuraPC_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to figuraPC_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help figuraPC

% Last Modified by GUIDE v2.5 13-Jan-2017 18:29:10

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @figuraPC_OpeningFcn, ...
                   'gui_OutputFcn',  @figuraPC_OutputFcn, ...
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


% --- Executes just before figuraPC is made visible.
function figuraPC_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to figuraPC (see VARARGIN)

% Choose default command line output for figuraPC
handles.output = hObject;
global RadiosCobertura;
global Prob;
global buttonPC;
buttonPC = 1;
dibujoCeldas(handles.axes1);
r = RadiosCobertura;
proa = sprintf('%.2f',Prob);

r1 = sprintf('%.2f m',r(1));
r2 = sprintf('%.2f m',r(2));
r3 = sprintf('%.2f m',r(3));
r4 = sprintf('%.2f m',r(4));

set(handles.proa,'String',proa);
set(handles.Rd1,'String', r1);
set(handles.Rd2,'String', r2);
set(handles.Rd3,'String', r3);
set(handles.Rd4,'String', r4);

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes figuraPC wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = figuraPC_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes during object creation, after setting all properties.
function axes1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: place code in OpeningFcn to populate axes1

% --- Executes when selected object is changed in panel.
function panel_SelectionChangeFcn(hObject, eventdata, handles)
% hObject    handle to the selected object in panel 
% eventdata  structure with the following fields (see UIBUTTONGROUP)
%	EventName: string 'SelectionChanged' (read only)
%	OldValue: handle of the previously selected object or empty if none was selected
%	NewValue: handle of the currently selected object
% handles    structure with handles and user data (see GUIDATA)
global buttonPC;
global RadiosCobertura;
global RadiosCoberturacl;
global Prob;
global Probcl;
if (hObject==handles.ol)
    buttonPC = 1;
    r = RadiosCobertura;
    proa = sprintf('%.2f',Prob);
    cla;
    dibujoCeldas(handles.axes1);
    r1 = sprintf('%.2f m',r(1));
    r2 = sprintf('%.2f m',r(2));
    r3 = sprintf('%.2f m',r(3));
    r4 = sprintf('%.2f m',r(4));

    set(handles.proa,'String',proa);
    set(handles.Rd1,'String', r1);
    set(handles.Rd2,'String', r2);
    set(handles.Rd3,'String', r3);
    set(handles.Rd4,'String', r4);
elseif (hObject==handles.cl)
    buttonPC = 2;
    r = RadiosCoberturacl;
    proa = sprintf('%.2f',Probcl);
    cla;
    dibujoCeldas(handles.axes1);
    r1 = sprintf('%.2f m',r(1));
    r2 = sprintf('%.2f m',r(2));
    r3 = sprintf('%.2f m',r(3));
    r4 = sprintf('%.2f m',r(4));

    set(handles.proa,'String',proa);
    set(handles.Rd1,'String', r1);
    set(handles.Rd2,'String', r2);
    set(handles.Rd3,'String', r3);
    set(handles.Rd4,'String', r4);
end
