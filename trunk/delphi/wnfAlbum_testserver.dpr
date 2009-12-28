program wnfAlbum_testserver;

uses
  Forms,
  wnfAlbum_testserver_main in 'wnfAlbum_testserver_main.pas' {Form1},
  wnfAlbumMain in 'wnfAlbumMain.pas' {dmMain: TDataModule},
  wnfAlbumSetup in 'wnfAlbumSetup.pas' {fmSetup},
  wnfAlbumTools in 'wnfAlbumTools.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TForm1, Form1);
  Application.CreateForm(TdmMain, dmMain);
  Application.Run;
end.
