function varargout = FiguraPTX(varargin)
% FIGURAPTX MATLAB code for FiguraPTX.fig
%      FIGURAPTX, by itself, creates a new FIGURAPTX or raises the existing
%      singleton*.
%
%      H = FIGURAPTX returns the handle to a new FIGURAPTX or the handle to
%      the existing singleton*.
%
%      FIGURAPTX('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FIGURAPTX.M with the given input arguments.
%
%      FIGURAPTX('Property','Value',...) creates a new FIGURAPTX or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before FiguraPTX_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to FiguraPTX_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help FiguraPTX

% Last Modified by GUIDE v2.5 21-Apr-2017 08:53:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @FiguraPTX_OpeningFcn, ...
                   'gui_OutputFcn',  @FiguraPTX_OutputFcn, ...
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


% --- Executes just before FiguraPTX is made visible.
function FiguraPTX_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to FiguraPTX (see VARARGIN)

% Choose default command line output for FiguraPTX
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
axes(handles.axes4);
handles.imagen = imread('NumCel.png');
imagesc(handles.imagen)
axis off;
% UIWAIT makes FiguraPTX wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = FiguraPTX_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in graptx.
function graptx_Callback(hObject, eventdata, handles)
% hObject    handle to graptx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
A = get(handles.cel,'Value');
B = str2double(get(handles.nue,'String'));
global rept;
global nues;
load ValoresPTX.mat PTXUEol Ptransmision SINRol SINRcl;
estadool =get(handles.ol,'Value');
estadoclol=get(handles.clol,'Value');
if(B<0||B>nues*3)
    %mensaje error
    errordlg('El Equipo Usuario no Existe','Error');
elseif isnan(B)
    warndlg('No ha ingresado el #UE','Advertencia');
else
if estadool == 1
     Potencia =PTXUEol;
     SI=SINRol;
elseif estadoclol == 1
     Potencia =Ptransmision;   
     SI=SINRcl;
 end

x = zeros (1,rept);
xsir=zeros(1,rept);
%u = zeros (1,rept);
intervalo = 1:1:rept;
for i=1:rept
    y = Potencia(i).ue;
    x(i)=y(B,A); 
    
    ysir=SI(i).ue;
    xsir(i)=ysir(B,A);
end
axes(handles.axes1);
xlabel('Iteraciones');
ylabel('Potencia de Transmisión [dBm]');
col =rand(1,3);
plot(intervalo, x,'Color',col,'linewidth',2,'DisplayName',['UE' int2str(B) ,',C' int2str(A)]);
z = (rand*rept);
w = x(round(z));
text(z,w,['UE' int2str(B) ,',C' int2str(A)],'color',col);
legend('off');
legend('show');
hold on;

axes(handles.axes3);
xlabel('Iteraciones');
ylabel('SINR [dB]');
plot(intervalo,xsir,'Color',col,'linewidth',3,'DisplayName',['UE' int2str(B) ,',C' int2str(A)]);
wsir=xsir(round(z));
text(z,wsir,['UE' int2str(B) ,',C' int2str(A)],'color',col);
legend('off');
legend('show');
hold on;
end
% --- Executes on button press in borra.
function borra_Callback(hObject, eventdata, handles)
% hObject    handle to borra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
legend('off');
axes(handles.axes1);
cla;
legend('off');
axes(handles.axes3);
cla;


% --- Executes on selection change in cel.
function cel_Callback(hObject, eventdata, handles)
% hObject    handle to cel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hints: contents = cellstr(get(hObject,'String')) returns cel contents as cell array
%        contents{get(hObject,'Value')} returns selected item from cel


% --- Executes during object creation, after setting all properties.
function cel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to cel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function nue_Callback(hObject, eventdata, handles)
% hObject    handle to nue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of nue as text
%        str2double(get(hObject,'String')) returns contents of nue as a double

% --- Executes during object creation, after setting all properties.
function nue_CreateFcn(hObject, eventdata, handles)
% hObject    handle to nue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes during object creation, after setting all properties.
function uipanel2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to uipanel2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes when selected object is changed in uipanel2.
function uipanel2_SelectionChangeFcn(hObject, eventdata, handles)
% hObject    handle to the selected object in uipanel2 
% eventdata  structure with the following fields (see UIBUTTONGROUP)
%	EventName: string 'SelectionChanged' (read only)
%	OldValue: handle of the previously selected object or empty if none was selected
%	NewValue: handle of the currently selected object
% handles    structure with handles and user data (see GUIDATA)
