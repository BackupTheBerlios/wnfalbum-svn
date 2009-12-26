unit wnfAlbumMain;

interface

uses
  SysUtils, Classes, IdBaseComponent, IdComponent, IdCustomTCPServer, IdContext,
  IdCustomHTTPServer, IdHTTPServer, dsp_Template, Forms, dsp_json;

type
  TdmMain = class(TDataModule)
    http: TIdHTTPServer;
    procedure DataModuleCreate(Sender: TObject);
    procedure DataModuleDestroy(Sender: TObject);
    procedure httpCommandGet(AContext: TIdContext;
      ARequestInfo: TIdHTTPRequestInfo; AResponseInfo: TIdHTTPResponseInfo);
  private
    FHTML: TdspTemplateCache;
    FAlben :Array of Record
      Name :string;
      Pfad :string;
    end;
    procedure AuswertungQ(json :TdspJSONObject; url :string);
  public
    procedure Start;
    procedure Einstellungen;
  end;

var
  dmMain: TdmMain;

implementation

{$R *.dfm}

uses dsp_ini, wnfAlbumSetup, dsp_tools;

resourcestring
  stError404 = 'Seite nicht gefunden';

procedure TdmMain.AuswertungQ(json: TdspJSONObject; url: string);
var
  I: Integer;
  alben :TdspJSONArray;
begin
  if url='album' then begin
    alben:=json.asArray['Alben'];
    for I := 0 to length(FAlben) - 1 do
      with alben.AddObject do begin
        asInteger['Album']:=I+1;
        asString['Name']:=FAlben[i].Name;
      end;
  end;

end;

procedure TdmMain.DataModuleCreate(Sender: TObject);
var
  s: string;
begin
  s:=ExtractFilePath(Application.ExeName);
  ForceDirectories(s+'cache\');
    FHTML := TdspTemplateCache.Create(s + 'www\');
 Start;
end;

procedure TdmMain.DataModuleDestroy(Sender: TObject);
begin
  FreeAndNil(FHTML);
end;

procedure TdmMain.Einstellungen;
begin
  ShowModalForm(TfmSetup);
  Start;
end;

procedure TdmMain.httpCommandGet(AContext: TIdContext; ARequestInfo: TIdHTTPRequestInfo; AResponseInfo: TIdHTTPResponseInfo);
var
  s: string;
  c: TdspFileCache;
  json :TdspJSONObject;
begin
  s := lowercase(ARequestInfo.Document);
  if pos('/q/', s) = 1 then begin
    json:=TdspJSONObject.Create;
    try
      AResponseInfo.ResponseNo := 200;
      Delete(s,1,3);
      AuswertungQ(json,s);
      AResponseInfo.ContentStream := json.UTF8toStream;
      json.UTF8toStream
    finally
      json.Free;
    end;
  end
  else begin

    c := FHTML.Find(s);
    if c <> nil then begin
      AResponseInfo.ResponseNo := 200;
      ARequestInfo.LastModified := c.FileAge;
      AResponseInfo.ContentStream := c.UTF8Stream;
    end
    else begin
      AResponseInfo.ResponseNo := 404;
      AResponseInfo.ContentText := stError404;
    end;
  end;
end;

procedure TdmMain.Start;
var
  I :integer;
  l :integer;
begin
  http.Active:=false;
  http.Bindings[0].Port:=IniDatei.ReadInteger('Einstellungen','Port',80);
  http.Active:=true;
  l:=IniDatei.ReadInteger('Alben','Anzahl',0);
  SetLength(FAlben,l);
  for I := 0 to l-1 do begin
    FAlben[I].Name:=IniDatei.ReadString('Alben',Format('Name%d',[I+1]),'');
    FAlben[I].Pfad:=IniDatei.ReadString('Alben',Format('Pfad%d',[I+1]),'');
  end;
end;

end.

