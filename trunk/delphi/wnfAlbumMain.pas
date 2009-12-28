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
    FAlben: array of record
      Name: string;
      Pfad: string;
    end;
    procedure AuswertungQ(json: TdspJSONObject; url: string; params: TStrings);
  public
    procedure Start;
    procedure Einstellungen;
  end;

var
  dmMain: TdmMain;

implementation

{$R *.dfm}

uses iniFiles, dsp_ini, wnfAlbumSetup, wnfAlbumTools, dsp_tools;

resourcestring
  stError404 = 'Seite nicht gefunden';

procedure TdmMain.AuswertungQ(json: TdspJSONObject; url: string; params: TStrings);
var
  I: Integer;
  arr: TdspJSONArray;
  pfad: string;
  jahr: string;
  monat: string;
  L: TStrings;
  s, n: string;
  monate: array[1..12] of boolean;
begin
  json.asString['URL'] := url;
  json.asString['Params'] := params.CommaText;
  if length(FAlben) > 0 then begin
    if url = 'album' then begin
      arr := json.asArray['Alben'];
      for I := 0 to length(FAlben) - 1 do
        with arr.AddObject do begin
          asInteger['Album'] := I;
          asString['Name'] := FAlben[i].Name;
        end;
    end
    else begin
      pfad := IncludeTrailingPathDelimiter(FAlben[StrToIntDef(params.Values['Album'], 0)].Pfad);
      if url = 'jahre' then begin
        arr := json.asArray['Jahre'];
        L := getAllDir(pfad, '????');
        try
          for S in L do
            if StrToIntDef(s, 0) > 0 then
              arr.AddObject.asString['Jahr'] := s;
        finally
          L.Free;
        end;
      end
      else begin
        jahr := params.Values['Jahr'];
        pfad := IncludeTrailingPathDelimiter(pfad+jahr);
        if url = 'monat' then begin
          arr := json.asArray['Monate'];
          FillChar(Monate, SizeOf(Monate), 0);
          L := getAllDir(pfad, jahr + '*');
          try
            for S in L do begin
              i := StrToIntDef(Copy(s, 5, 2), 0);
              if i in [1..12] then
                monate[i] := true;
            end;
          finally
            L.Free;
          end;
          for I := 1 to 12 do
            if monate[i] then
              with arr.AddObject do begin
                asInteger['Monat'] := i;
                asString['Name'] := LongMonthNames[i];
              end;
        end
        else begin
          monat := params.Values['Monat'];
          while length(monat) < 2 do monat := '0' + monat;
          if url = 'tage' then begin
            arr := json.asArray['Tage'];
            L := getAllDir(pfad, jahr + monat + '*');
            try
              for S in L do
                with arr.AddObject do begin
                  n := copy(s, 7, 2) + ' - ';
                  if FileExists(pfad+ s + '\' + 'album.dat') then begin
                    with TIniFile.Create(pfad + s + '\' + 'album.dat') do
                    try
                      n := n + ReadString('Titel', 'Titelname', '');
                    finally
                      Free;
                    end;
                  end
                  else
                    if pos(' ', s) > 8 then
                      n := n + copy(s, pos(' ', s) + 1, 255);
                  asString['Name'] := n;
                  asString['Verzeichnis'] := s;
                end;
            finally
              L.Free;
            end;
          end
          else begin
            pfad:=IncludeTrailingPathDelimiter(Pfad+params.Values['Tag']);
            if url = 'bilder' then begin
              arr := json.asArray['Bilder'];
              L:=TStringList.Create;
              try
                (l as TStringList).Sorted:=true;
                FindFiles(L,pfad,'*.jpg');
              for S in L do
                with arr.AddObject do begin
                  asString['Bild']:=s;
                end;
              finally
                L.Free;
              end;
            end;
          end;
        end;
      end;
    end;
  end;
end;

procedure TdmMain.DataModuleCreate(Sender: TObject);
var
  s: string;
begin
  s := ExtractFilePath(Application.ExeName);
  ForceDirectories(s + 'cache\');
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
  json: TdspJSONObject;
begin
  s := lowercase(ARequestInfo.Document);
  if pos('/q/', s) = 1 then begin
    json := TdspJSONObject.Create;
    try
      AResponseInfo.ResponseNo := 200;
      Delete(s, 1, 3);
      AuswertungQ(json, s, ARequestInfo.Params);
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
  I: integer;
  l: integer;
begin
  http.Active := false;
  http.DefaultPort := IniDatei.ReadInteger('Einstellungen', 'Port', 80);
  http.Active := true;
  l := IniDatei.ReadInteger('Alben', 'Anzahl', 0);
  SetLength(FAlben, l);
  for I := 0 to l - 1 do begin
    FAlben[I].Name := IniDatei.ReadString('Alben', Format('Name%d', [I + 1]), '');
    FAlben[I].Pfad := IniDatei.ReadString('Alben', Format('Pfad%d', [I + 1]), '');
  end;
end;

end.

