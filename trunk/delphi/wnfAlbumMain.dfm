object dmMain: TdmMain
  OldCreateOrder = False
  OnCreate = DataModuleCreate
  OnDestroy = DataModuleDestroy
  Height = 171
  Width = 287
  object http: TIdHTTPServer
    Active = True
    Bindings = <
      item
        IP = '127.0.0.1'
        Port = 80
      end>
    AutoStartSession = True
    OnCommandGet = httpCommandGet
    Left = 40
    Top = 32
  end
end
