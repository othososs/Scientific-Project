Function ExtractDateFromFileName(fileName As String) As String
    ' Extrait la date du nom de fichier au format "DYYMMDD"
    Dim startPos As Integer
    Dim endPos As Integer
    
    startPos = InStr(fileName, "D")
    
    If startPos > 0 Then
        endPos = startPos + 6 ' La date est toujours composée de 6 caractères après le "D"
        ExtractDateFromFileName = Mid(fileName, startPos + 1, 6)
    Else
        ' Retourne une chaîne vide si "D" n'est pas trouvé
        ExtractDateFromFileName = ""
    End If
End Function
