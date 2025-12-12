; CameraLocker Inno Setup Script з автозапуском

[Setup]
AppName=Camera Locker
AppVersion=1.0
AppPublisher=Oleg
AppPublisherURL=https://github.com/yourusername/CameraLocker
DefaultDirName={pf}\CameraLocker
DefaultGroupName=Camera Locker
OutputDir=dist_installer
OutputBaseFilename=CameraLockerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=icon.ico

[Files]
Source: "dist\CameraLocker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Camera Locker"; Filename: "{app}\CameraLocker.exe"
Name: "{commondesktop}\Camera Locker"; Filename: "{app}\CameraLocker.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Створити ярлик на робочому столі"; GroupDescription: "Додаткові опції"; Flags: unchecked

[Run]
Filename: "{app}\CameraLocker.exe"; Description: "Запустити Camera Locker"; Flags: nowait postinstall skipifsilent

[Registry]
; Автозапуск при вході користувача
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "CameraLocker"; ValueData: """{app}\CameraLocker.exe"""; Flags: uninsdeletevalue