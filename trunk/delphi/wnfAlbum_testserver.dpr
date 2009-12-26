program wnfAlbum_testserver;

uses
  Forms,
  wnfAlbum_testserver_main in 'wnfAlbum_testserver_main.pas' {Form1};

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TForm1, Form1);
  Application.Run;
end.
