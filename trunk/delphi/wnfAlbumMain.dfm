object dmMain: TdmMain
  OldCreateOrder = False
  OnCreate = DataModuleCreate
  OnDestroy = DataModuleDestroy
  Height = 171
  Width = 287
  object http: TIdHTTPServer
    Bindings = <>
    AutoStartSession = True
    ServerSoftware = 'wnfAlbum'
    OnCommandGet = httpCommandGet
    Left = 40
    Top = 32
  end
end
