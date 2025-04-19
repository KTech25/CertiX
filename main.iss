[Setup]
; Basic settings
AppName=CertiX
AppVersion=2.0
DefaultDirName={pf}\certificate-generator
DefaultGroupName=CertiX
OutputDir=output
OutputBaseFilename=CertiX_Installer
Compression=lzma
SolidCompression=yes

[Files]
; The executable and any additional files
Source: "dist\main\CertiX.exe"; DestDir: "{app}\main"; Flags: ignoreversion
Source: "dist\main\_internal\python313.dll"; DestDir: "{app}\main\_internal"; Flags: ignoreversion

[Icons]
Name: "{group}\CertiX"; Filename: "{app}\main\CertiX.exe"
Name: "{userdesktop}\CertiX"; Filename: "{app}\main\CertiX.exe"

[Run]
; Execute the application after installation
Filename: "{app}\main\CertiX.exe"; Description: "{cm:LaunchProgram,CertiX}"; Flags: nowait postinstall skipifsilent
