object fmSetup: TfmSetup
  Left = 0
  Top = 0
  BorderStyle = bsToolWindow
  Caption = 'Einstellungen'
  ClientHeight = 293
  ClientWidth = 569
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  Position = poScreenCenter
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 16
    Top = 4
    Width = 24
    Height = 13
    Caption = 'Port:'
    FocusControl = edPort
  end
  object edPort: TSpinEdit
    Left = 16
    Top = 19
    Width = 71
    Height = 22
    Constraints.MinHeight = 22
    MaxValue = 9999
    MinValue = 1
    TabOrder = 0
    Value = 80
  end
  object lvAlben: TListView
    Left = 93
    Top = 19
    Width = 468
    Height = 150
    Columns = <
      item
        Caption = 'Name'
        Width = 120
      end
      item
        AutoSize = True
        Caption = 'Verzeichnis'
      end>
    TabOrder = 1
    ViewStyle = vsReport
  end
  object edName: TEdit
    Left = 16
    Top = 192
    Width = 121
    Height = 21
    TabOrder = 2
    TextHint = 'Albumname'
    OnChange = edNameChange
  end
  object edDir: TdspDirectoryEdit
    Left = 143
    Top = 192
    Width = 337
    Height = 21
    TabOrder = 3
    TextHint = 'Bitte Verzeichnis asuw'#228'hlen'
    OnChange = edNameChange
  end
  object btnAdd: TButton
    Left = 486
    Top = 190
    Width = 75
    Height = 25
    Caption = 'Hinzuf'#252'gen'
    Enabled = False
    TabOrder = 4
    OnClick = btnAddClick
  end
  object Button1: TButton
    Left = 405
    Top = 260
    Width = 75
    Height = 25
    Caption = 'Speichern'
    ModalResult = 1
    TabOrder = 5
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 486
    Top = 260
    Width = 75
    Height = 25
    Caption = 'Abbrechen'
    ModalResult = 2
    TabOrder = 6
  end
end
