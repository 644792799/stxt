Attribute VB_Name = "Module2"
Sub �������Ʀr��()
'
' Macro1 Macro
' �i²�W�� �b 2013/1/3 ���s������
'
    Dim vCNum(1 To 12) As Variant
    vCNum(1) = "�@"
    vCNum(2) = "�G"
    vCNum(3) = "�T"
    vCNum(4) = "�|"
    vCNum(5) = "��"
    vCNum(6) = "��"
    vCNum(7) = "�C"
    vCNum(8) = "�K"
    vCNum(9) = "�E"
    vCNum(10) = "�Q"
    vCNum(11) = "�Q�@"
    vCNum(12) = "�Q�G"

    For i = 12 To 1 Step -1
        cMon = vCNum(i) & "��"
        nMon = i & "��"
        Cells.Replace What:=cMon, Replacement:=nMon, _
                             LookAt:=xlPart, SearchOrder:=xlByRows, _
                             MatchCase:=False, SearchFormat:=False, _
                             ReplaceFormat:=False
    Next
End Sub

