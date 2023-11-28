Sub MiseAJourFichiersNouveaux()
    Dim ws As Worksheet
    Dim col As Range
    Dim currentDate As String
    Dim sourceFilePath As String
    Dim filterValue As String
    Dim rowCount As Long
    
    ' Spécifiez ici le répertoire où se trouvent vos fichiers sources
    Const sourceDirectory As String = "C:\CheminetDeVotreDossier\"

    ' Spécifiez ici la ligne où se trouvent les dates et la ligne où vous souhaitez placer les sommes
    Const datesRow As Integer = 1

    ' Obtenez la feuille de calcul active (vous pouvez également spécifier une feuille spécifique)
    Set ws = ActiveSheet

    ' Boucle sur les colonnes de la première ligne (E à AA)
    For Each col In ws.Range("E:AA").Columns
        ' Récupère la date de la colonne actuelle
        currentDate = ExtractDateFromFileName(ws.Cells(datesRow, col.Column).Value)
        
        ' Génère le nom de fichier source
        sourceFilePath = sourceDirectory & "Cr_maj_valeurs_" & currentDate & "_T" & col.Column & ".xlsx"

        ' Vérifie si le fichier source existe
        If Dir(sourceFilePath) <> "" Then
            ' Ouvre le fichier source
            Workbooks.Open sourceFilePath

            ' Applique un filtre dans la colonne E pour sélectionner "A controler"
            ws.Columns("E").AutoFilter Field:=1, Criteria1:="A controler"

            ' Compte le nombre de lignes filtrées (à l'exception de la ligne d'en-tête)
            rowCount = ws.AutoFilter.Range.Columns(1).SpecialCells(xlCellTypeVisible).Cells.Count - 1

            ' Place le nombre de lignes dans le fichier d'origine à la colonne de la date correspondante et à la ligne 1
            ws.Cells(1, col.Column).Value = rowCount

            ' Désactive le filtre
            ws.AutoFilterMode = False

            ' Ferme le fichier source sans sauvegarder les modifications
            ActiveWorkbook.Close False
        Else
            ' Affiche un message d'avertissement si le fichier source n'est pas trouvé
            MsgBox "Le fichier source pour la date " & currentDate & " n'a pas été trouvé.", vbExclamation
        End If
    Next col
End Sub

Function ExtractDateFromFileName(fileName As String) As String
    ' Extrait la date du nom de fichier au format "DYYMMDD"
    Dim startPos As Integer
    Dim endPos As Integer
    startPos = InStr(fileName, "D") + 1
    endPos = InStr(startPos, fileName, "_") - 1
    ExtractDateFromFileName = Mid(fileName, startPos, endPos - startPos + 1)
End Function
