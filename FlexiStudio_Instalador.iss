#define Nombre "Flexi Studio"
#define Version "1.1.0"
#define Ejecutable "FlexiStudio.exe"

[Setup]
AppId={{6E914CF4-1F2B-4BAF-9A87-10EA68F5B404}
AppName={#Nombre}
AppVersion={#Version}
AppPublisher=Proyecto académico Flexi Zamora
DefaultDirName={localappdata}\Programs\Flexi Studio
DefaultGroupName=Flexi Studio
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=salida
OutputBaseFilename=FlexiStudio_Setup_1.1.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\flexi.ico
UninstallDisplayIcon={app}\FlexiStudio.exe
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: checkedonce

[Files]
Source: "dist\FlexiStudio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userprograms}\Flexi Studio"; Filename: "{app}\{#Ejecutable}"; WorkingDir: "{app}"
Name: "{userprograms}\Configurar conexiones de Flexi Studio"; Filename: "{app}\{#Ejecutable}"; Parameters: "--configurar"; WorkingDir: "{app}"
Name: "{userdesktop}\Flexi Studio"; Filename: "{app}\{#Ejecutable}"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "{app}\{#Ejecutable}"; Description: "Abrir Flexi Studio"; Flags: nowait postinstall skipifsilent
