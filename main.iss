[Setup]
; Basic settings
AppName=CertiX
AppVersion=1.0
DefaultDirName={pf}\certificate-generator
DefaultGroupName=CertiX
OutputDir=output
OutputBaseFilename=CertiX_Installer
Compression=lzma
SolidCompression=yes

[Files]
; The executable and any additional files
Source: "dist\CertiX.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
Name: "{group}\CertiX"; Filename: "{app}\CertiX.exe"
Name: "{userdesktop}\CertiX"; Filename: "{app}\CertiX.exe"

[Run]
; Execute the application after installation
Filename: "{app}\CertiX.exe"; Description: "{cm:LaunchProgram,CertiX}"; Flags: nowait postinstall skipifsilent
