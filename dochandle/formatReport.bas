Attribute VB_Name = "NewMacros"
Type RenameDef
    OldName As String
    NewName As String
End Type

Sub ���ɦҮ֮榡()
    Call ����άA������
    Call ���D�ǩ�
End Sub

Sub ����άA������()
'
' ����άA������ ����
' �������s�� 2011/12/19�A���s�� �i²�W��
'
    Selection.Find.ClearFormatting
    With Selection.Find
        .Text = "�u*�v"
        .Forward = True
        .Wrap = wdFindContinue
        .Format = True
        .MatchWildcards = True
    End With
    Do
      Selection.Find.Execute
      Selection.Font.Bold = True
    Loop While Selection.Find.Found
    
    With Selection.Find
        .Text = "(����[0-9]{1,}*)"
        .Forward = True
        .Wrap = wdFindContinue
        .Format = True
        .MatchWildcards = True
    End With
    Do
      Selection.Find.Execute
      Selection.Font.Bold = True
    Loop While Selection.Find.Found
    
End Sub

Sub ���D�ǩ�()
' ����2 ����
' �������s�� 2013/1/7�A���s�� �i²�W��
'
    Selection.Find.ClearFormatting
    With Selection.Find
        .Text = "([�@�G�T�|�����C�K�E�Q].*�H)"
        .Forward = True
        .Wrap = wdFindContinue
        .Format = True
        .MatchWildcards = True
    End With
        
    Do
      Selection.Find.Execute
      Selection.Paragraphs(1).Shading.BackgroundPatternColor = wdColorGray15
      Selection.Font.Bold = False
    Loop While Selection.Find.Found
    
End Sub

Sub ��w��󭫩R�W()
Attribute ��w��󭫩R�W.VB_Description = "�������s�� 2013/1/16�A���s�� �i²�W��"
Attribute ��w��󭫩R�W.VB_ProcData.VB_Invoke_Func = "Normal.NewMacros.��w��󭫩R�W"
    Dim renames(2) As RenameDef
    renames(1).OldName = "�i�������Ρj"
    renames(1).NewName = "�Ὤ���a��|�ȧ�"
    renames(2).OldName = "�����N�X"
    renames(2).NewName = "HLTB"
    
    For i = 1 To 2
        Dim r As RenameDef
        r = renames(i)
        Selection.Find.ClearFormatting
        Selection.Find.Replacement.ClearFormatting
        With Selection.Find
            .Text = r.OldName
            .Replacement.Text = r.NewName
            .Forward = True
        End With
        Selection.Find.Execute Replace:=wdReplaceAll
    Next i

End Sub
