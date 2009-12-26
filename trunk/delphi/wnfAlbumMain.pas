unit wnfAlbumMain;

interface

uses
  SysUtils, Classes, IdBaseComponent, IdComponent, IdCustomTCPServer, IdContext,
  IdCustomHTTPServer, IdHTTPServer, dsp_Template, forms;

type
  TdmMain = class(TDataModule)
    http: TIdHTTPServer;
    procedure DataModuleCreate(Sender: TObject);
    procedure DataModuleDestroy(Sender: TObject);
    procedure httpCommandGet(AContext: TIdContext;
      ARequestInfo: TIdHTTPRequestInfo; AResponseInfo: TIdHTTPResponseInfo);
  private
    FHTML: TdspTemplateCache;
  public
    { Public-Deklarationen }
  end;

var
  dmMain: TdmMain;

implementation

{$R *.dfm}

resourcestring
  stError404 = 'Seite nicht gefunden';

procedure TdmMain.DataModuleCreate(Sender: TObject);
var
  s: string;
begin
  s:=ExtractFilePath(Application.ExeName);
  ForceDirectories(s+'cache\');
    FHTML := TdspTemplateCache.Create(s + 'www\');
end;

procedure TdmMain.DataModuleDestroy(Sender: TObject);
begin
  FreeAndNil(FHTML);
end;

procedure TdmMain.httpCommandGet(AContext: TIdContext; ARequestInfo: TIdHTTPRequestInfo; AResponseInfo: TIdHTTPResponseInfo);
var
  s: string;
  c: TdspFileCache;
begin
  s := lowercase(ARequestInfo.Document);
  if pos('/q/', s) = 1 then begin

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

end.

