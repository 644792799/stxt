Attribute VB_Name = "NewMacros"
Sub ����άA������()
Attribute ����άA������.VB_Description = "�������s�� 2011/12/19�A���s�� �i²�W��"
Attribute ����άA������.VB_ProcData.VB_Invoke_Func = "Normal.NewMacros.����άA������"
'
' ����άA������ ����
' �������s�� 2011/12/19�A���s�� �i²�W��
'
    Selection.Find.Execute Replace:=wdReplaceAll
    With Selection.Find
        .Text = "�u*�v"
        .Replacement.Text = ""
        .Forward = True
        .Wrap = wdFindContinue
        .Format = True
        .MatchCase = False
        .MatchWholeWord = False
        .MatchByte = False
        .CorrectHangulEndings = False
        .MatchAllWordForms = False
        .MatchSoundsLike = False
        .MatchFuzzy = False
        .MatchWildcards = True
    End With
    Selection.Find.Execute Replace:=wdReplaceAll
    With Selection.Find
        .Text = "\(�p����*\)"
        .Replacement.Text = ""
        .Forward = True
        .Wrap = wdFindContinue
        .Format = True
        .MatchCase = False
        .MatchWholeWord = False
        .MatchByte = False
        .CorrectHangulEndings = False
        .MatchAllWordForms = False
        .MatchSoundsLike = False
        .MatchFuzzy = False
        .MatchWildcards = True
    End With
    Selection.Find.Execute Replace:=wdReplaceAll
End Sub
