Attribute VB_Name = "Module1"
Sub �ץX���Ѫ���妸��()
Attribute �ץX���Ѫ���妸��.VB_Description = "�i²�W�� �b 2013/1/23 ���s������"
Attribute �ץX���Ѫ���妸��.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro1 Macro
' �i²�W�� �b 2013/1/23 ���s������
'
    Dim sdir, tdir, ps() As String
    sdir = "\\eee\kms_files\Upload"
    tdir = "d:\kmexport\testfile"
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set f = fs.CreateTextFile("c:\export_kmfile.bat", True)
    
    For Each w In Worksheets
        With w.Cells
            Set c = .Find("km", LookIn:=xlValues)
            If Not c Is Nothing Then
                firstAddress = c.Address
                Do
                    ps = Split(CStr(c.Value), Chr(10))
                    For i = 1 To UBound(ps)
                        If ps(i) <> "" Then
                            s = sdir & ps(i)
                            t = tdir & ps(i)
                            p = "copy " & s & " " & t
                            f.WriteLine p
                        End If
                    Next
                    Set c = .FindNext(c)
                Loop While Not c Is Nothing And c.Address <> firstAddress
            End If
        End With
    Next
    f.Close

End Sub
