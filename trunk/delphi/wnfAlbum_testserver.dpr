program wnfAlbum_testserver;

uses
  Forms,
  wnfAlbum_testserver_main in 'wnfAlbum_testserver_main.pas' {Form1},
  wnfAlbumMain in 'wnfAlbumMain.pas' {dmMain: TDataModule};

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TForm1, Form1);
  Application.CreateForm(TdmMain, dmMain);
  Application.Run;
end.
