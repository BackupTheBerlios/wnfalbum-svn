unit wnfAlbumTools;

interface

uses SysUtils, Classes;

function getAllDir(pfad, maske: string): TStrings;

implementation


function getAllDir(pfad, maske: string): TStrings;
var
  R: TSearchRec;
begin
  if maske='' then maske:='*.*';
  Result := TStringList.Create;
  (Result as TStringList).Sorted := true;
  if FindFirst(IncludeTrailingPathDelimiter(Trim(pfad))+maske+'*.*', faDirectory, R) = 0 then begin
    repeat
      Result.Add(R.Name);
    until FindNext(R) <> 0;
    FindClose(R);
  end;

end;

end.

