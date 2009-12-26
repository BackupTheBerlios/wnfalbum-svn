unit wnfAlbumSetup;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Spin, ExtCtrls, dspButtonEdit, ComCtrls;

type
  TfmSetup = class(TForm)
    edPort: TSpinEdit;
    Label1: TLabel;
    lvAlben: TListView;
    edName: TEdit;
    edDir: TdspDirectoryEdit;
    btnAdd: TButton;
    Button1: TButton;
    Button2: TButton;
    procedure edNameChange(Sender: TObject);
    procedure btnAddClick(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
  private
    { Private-Deklarationen }
  public
    { Public-Deklarationen }
  end;

implementation

{$R *.dfm}

uses dsp_tools, dsp_ini;

procedure TfmSetup.btnAddClick(Sender: TObject);
begin
  with lvAlben.Items.Add do begin
    Caption:=edName.Text;
    SubItems.Add(edDir.Text);
  end;
  edName.Text:='';
  edDir.Text:='';
end;

procedure TfmSetup.Button1Click(Sender: TObject);
var
  I: Integer;
begin
  IniDatei.WriteInteger('Einstellungen','Port',edPort.Value);
  IniDatei.WriteInteger('Alben','Anzahl',lvAlben.Items.Count);
  for I := 0 to lvAlben.Items.Count - 1 do begin
    IniDatei.WriteString('Alben',Format('Name%d',[I+1]),lvAlben.Items[i].Caption);
    IniDatei.WriteString('Alben',Format('Pfad%d',[I+1]),lvAlben.Items[i].SubItems[0]);
  end;
end;

procedure TfmSetup.edNameChange(Sender: TObject);
begin
  btnAdd.Enabled:=(trim(edName.Text)<>'') and (trim(edDir.Text)<>'') and (DirectoryExists(edDir.Text));
end;

procedure TfmSetup.FormCreate(Sender: TObject);
var
  I: Integer;
begin
  edPort.Value:=IniDatei.ReadInteger('Einstellungen','Port',80);
  for I := 0 to IniDatei.ReadInteger('Alben','Anzahl',0)-1 do
    with lvAlben.Items.Add do begin
    Caption:=IniDatei.ReadString('Alben',Format('Name%d',[I+1]),'');
    SubItems.Add(IniDatei.ReadString('Alben',Format('Pfad%d',[I+1]),''));
  end;
end;

end.
