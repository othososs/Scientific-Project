Function ExtractDateFromFileName(fileName As String) As String
    ' Extrait la date du nom de fichier au format "DYYMMDD"
    Dim startPos As Integer
    Dim endPos As Integer
    
    startPos = InStr(fileName, "Cr_maj_valeurs_") + Len("Cr_maj_valeurs_") + 1
    endPos = startPos + 5 ' La date est toujours composée de 6 caractères après "Cr_maj_valeurs_"
    
    If startPos > 0 Then
        ExtractDateFromFileName = Mid(fileName, startPos, 6)
    Else
        ' Retourne une chaîne vide si "Cr_maj_valeurs_" n'est pas trouvé
        ExtractDateFromFileName = ""
    End If
End Function
